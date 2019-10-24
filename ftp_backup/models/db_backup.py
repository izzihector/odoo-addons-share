# -*- coding: utf-8 -*-

import os
import time
import odoo
import base64
import socket
import logging
import datetime
import subprocess

from ftplib import FTP

from odoo import models, fields, api, tools, _
from odoo.exceptions import Warning
from odoo.http import content_disposition

_logger = logging.getLogger(__name__)

try:
    import paramiko
except ImportError:
    raise ImportError(
        'This module needs paramiko to automatically write '
        'backups to the FTP through SFTP. Please install paramiko '
        'on your system. (sudo pip3 install paramiko)')

try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib


def execute(connector, method, *args):
    """."""
    res = False
    try:
        res = getattr(connector, method)(*args)
    except socket.error as error:
        _logger.critical(
            'Error while executing the method "execute". Error: ' + str(error))
        raise error
    return res


class DbBackup(models.Model):
    """."""

    _inherit = 'db.backup'

    send_ftp = fields.Boolean(
        'Respaldo en FTP',
        help='Si selecciona esta opción, usted puede seleccionar '
        'automaticamente transferir el respaldo a un servidor ftp.')
    ftp_dest = fields.Char(
        'FTP Dest.',
        help="La ruta del servidor ftp")
    ftp_user = fields.Char('FTP Usuario', help="Usuario del servidor ftp")
    ftp_pwd = fields.Char(
        'FTP Contraseña', help="Contraseña del usuario del servidor ftp")

    @api.multi
    def schedule_backup(self):
        """."""
        conf_ids = self.search([])
        for rec in conf_ids:
            db_list = self.get_db_list(rec.host, rec.port)

            if rec.name in db_list:
                try:
                    if not os.path.isdir(rec.folder):
                        os.makedirs(rec.folder)
                except:
                    raise

                # Create name for dumpfile.
                company_name = self.env.user.company_id.name.replace(
                    " ", "_").replace(".", "_").lower()
                bkp_file = '%s_%s.%s' % (time.strftime(
                    '%Y_%m_%d_%H_%M_%S'), rec.name, rec.backup_type)
                bkp_file = company_name + '_' + bkp_file
                file_path = os.path.join(rec.folder, bkp_file)
                uri = 'http://' + rec.host + ':' + rec.port
                conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
                bkp = ''

                try:
                    # try to backup database and write it away
                    fp = open(file_path, 'wb')
                    odoo.service.db.dump_db(rec.name, fp, rec.backup_type)
                    fp.close()
                except Exception as error:
                    _logger.debug(
                        "Couldn't backup database %s. Bad database administrator password for server running at http://%s:%s" % (
                            rec.name, rec.host, rec.port))
                    _logger.debug(
                        "Exact error from the exception: " + str(error))
                    continue

            else:
                _logger.debug("database %s doesn't exist on http://%s:%s" %
                              (rec.name, rec.host, rec.port))

            # Check if user wants to write to SFTP or not.
            if rec.sftp_write is True:

                try:
                    # Store all values in variables
                    dir = rec.folder
                    pathToWriteTo = rec.sftp_path
                    ipHost = rec.sftp_host
                    portHost = rec.sftp_port
                    usernameLogin = rec.sftp_user
                    passwordLogin = rec.sftp_password

                    _logger.debug('sftp remote path: %s' % pathToWriteTo)

                    try:
                        s = paramiko.SSHClient()
                        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        s.connect(ipHost, portHost, usernameLogin,
                                  passwordLogin, timeout=20)
                        sftp = s.open_sftp()
                    except Exception as error:
                        _logger.critical(
                            'Error connecting to remote server! Error: ' + str(error))

                    try:
                        sftp.chdir(pathToWriteTo)
                    except IOError:
                        # Create directory and subdirs if they do not exist.
                        currentDir = ''
                        for dirElement in pathToWriteTo.split('/'):
                            currentDir += dirElement + '/'
                            try:
                                sftp.chdir(currentDir)
                            except:
                                _logger.info(
                                    '(Part of the) path didn\'t exist. Creating it now at ' + currentDir)
                                # Make directory and then navigate into it
                                sftp.mkdir(currentDir, 777)
                                sftp.chdir(currentDir)
                                pass
                    sftp.chdir(pathToWriteTo)
                    # Loop over all files in the directory.
                    for f in os.listdir(dir):
                        if rec.name in f:
                            fullpath = os.path.join(dir, f)
                            if os.path.isfile(fullpath):
                                try:
                                    sftp.stat(os.path.join(pathToWriteTo, f))
                                    _logger.debug(
                                        'File %s already exists on the remote FTP Server ------ skipped' % fullpath)
                                # This means the file does not exist (remote)
                                # yet!
                                except IOError:
                                    try:
                                        # sftp.put(fullpath, pathToWriteTo)
                                        sftp.put(fullpath, os.path.join(
                                            pathToWriteTo, f))
                                        _logger.info(
                                            'Copying File % s------ success' % fullpath)
                                    except Exception as err:
                                        _logger.critical(
                                            'We couldn\'t write the file to the remote server. Error: ' + str(err))

                    # Navigate in to the correct folder.
                    sftp.chdir(pathToWriteTo)

                    # Loop over all files in the directory from the back-ups.
                    # We will check the creation date of every back-up.
                    for file in sftp.listdir(pathToWriteTo):
                        if rec.name in file:
                            # Get the full path
                            fullpath = os.path.join(pathToWriteTo, file)
                            # Get the timestamp from the file on the external
                            # server
                            timestamp = sftp.stat(fullpath).st_atime
                            createtime = datetime.datetime.fromtimestamp(
                                timestamp)
                            now = datetime.datetime.now()
                            delta = now - createtime
                            # If the file is older than the days_to_keep_sftp
                            # (the days to keep that the user filled in on the
                            # Odoo form it will be removed.
                            if delta.days >= rec.days_to_keep_sftp:
                                # Only delete files, no directories!
                                if sftp.isfile(fullpath) and (".dump" in file or '.zip' in file):
                                    _logger.info(
                                        "Delete too old file from SFTP servers: " + file)
                                    sftp.unlink(file)
                    # Close the SFTP session.
                    sftp.close()
                except Exception as e:
                    _logger.debug(
                        'Exception! We couldn\'t back up to the FTP server..')
                    # At this point the SFTP backup failed. We will now check if the user wants
                    # an e-mail notification about this.
                    if rec.send_mail_sftp_fail:
                        try:
                            ir_mail_server = self.env['ir.mail_server']
                            message = "Dear,\n\nThe backup for the server " + rec.host + " (IP: " + rec.sftp_host + ") failed.Please check the following details:\n\nIP address SFTP server: " + rec.sftp_host + "\nUsername: " + rec.sftp_user + "\nPassword: " + rec.sftp_password + "\n\nError details: " + tools.ustr(
                                e) + "\n\nWith kind regards"
                            msg = ir_mail_server.build_email("auto_backup@" + rec.name + ".com", [rec.email_to_notify],
                                                             "Backup from " + rec.host +
                                                             "(" + rec.sftp_host +
                                                             ") failed",
                                                             message)
                            ir_mail_server.send_email(self._cr, self._uid, msg)
                        except Exception:
                            pass

            """
            Remove all old files (on local server) in case this is configured..
            """
            if rec.autoremove:
                dir = rec.folder
                # Loop over all files in the directory.
                for f in os.listdir(dir):
                    fullpath = os.path.join(dir, f)
                    # Only delete the ones wich are from the current database
                    # (Makes it possible to save different databases in the same folder)
                    if rec.name in fullpath:
                        timestamp = os.stat(fullpath).st_ctime
                        createtime = datetime.datetime.fromtimestamp(timestamp)
                        now = datetime.datetime.now()
                        delta = now - createtime
                        if delta.days >= rec.days_to_keep:
                            # Only delete files (which are .dump and .zip), no
                            # directories.
                            if os.path.isfile(fullpath) and (".dump" in f or '.zip' in f):
                                _logger.info(
                                    "Delete local out-of-date file: " + fullpath)
                                os.remove(fullpath)

            """
            Seccion FTP - MFH
            """
            if rec.send_ftp is True:
                print()
                print(file_path)
                print(rec.ftp_dest)
                print(rec.ftp_user)
                print(rec.ftp_pwd)
                print()
                try:
                    subprocess.check_output('curl -T %s ftp://%s --user %s:%s' % (
                        file_path, rec.ftp_dest, rec.ftp_user, rec.ftp_pwd), shell=True)
                    _logger.info(
                        _('Succesfully transfered backup to ftp server %s' % rec.ftp_dest))
                except Exception as e:
                    _logger.info(
                        _("Something went wrong!... Couldn't transfer db backup to ftp server"))
