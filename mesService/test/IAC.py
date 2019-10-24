# -*- coding: utf-8 -*-
# @createTime    : 2019/10/14 13:28
# @author  : Huanglg
# @fileName: IAC.py
# @email: luguang.huang@mabotech.com
from lxml import etree


class IACXML(object):

    def __init__(self, dict_data):
        self.dict_data = dict_data

    def generate_iac_xml(self):
        root = etree.Element("root")
        for k,v in self.dict_data.items():
            item = etree.SubElement(root, 'item')
            item.set("name", k)
            item.set("value", v)
        print(etree.tostring(root, pretty_print=True))
        tree = etree.ElementTree(root)
        tree.write('text.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == '__main__':
    dict_data = {
        "TransactionID":"POF",
        "Level1No":"5271866",
        "ParentNo":"5271867",
        "ChildNo":"5568155",
        "Qty":"1",
        "WorkStation":"47500",
        "EffectiveDate":"09/11/2019 00:00:00",
        "DiscontinueDate":"10/11/2019 00:00:00",
        "KittingStation":"0",
        "BulkWorkStation":"0",
        "ProductionLineNo":"38",
    }
    iacxml = IACXML(dict_data)
    iacxml.generate_iac_xml()
