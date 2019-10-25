# coding: utf-8
from lxml import etree


def deny_access(xml, path, option=('options', '{"no_create": 1, "no_open": 1}')):
    u"""
    Restringe el acceso de creación y edición a una vista ``xml``, sobre el
    campo encontrado en ``path``. Se puede dar una tupla diferente a la default
    en ``option`` para definir otro comportamiento (Cuidado con esto).
    """
    doc = etree.XML(xml)
    for node in doc.xpath(path):
        node.set(*option)
    return etree.tostring(doc)
