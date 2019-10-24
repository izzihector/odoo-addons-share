from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        new_args = []
        for arg in args:
            if isinstance(arg, (tuple, list)) and arg[0] in ['name', 'display_name'] and isinstance(arg[2], str):
                arg[2] = arg[2].replace(' ', '%')
            new_args.append(arg)
        partners = super().search(new_args, offset=offset, limit=limit, order=order, count=count)
        return partners
