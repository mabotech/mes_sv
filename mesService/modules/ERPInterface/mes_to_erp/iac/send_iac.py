# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com
import requests
from lxml import etree

from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class IacToXml(object):
    def __init__(self):
        self.root = etree.Element('root')
        self.db = self.create_conn('development')
        self.url = ''

    def dict_to_xml(self, dict_data):

        for k, v in dict_data.items():
            node = etree.SubElement(self.root, k)
            if v:
                node.text = str(v)

        tree = etree.ElementTree(self.root)
        tree.write('text.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
        xml_str = etree.tostring(tree, encoding='utf-8', pretty_print=True)
        return xml_str

    def get_iac_data(self):

        sql_str = "select get_iac();"
        result = self.db.query(sql_str)
        return result[0]['get_iac']

    def create_conn(self, config_name):
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

    def set_to_erp(self, xml):
        try:
            requests.post(
                url = self.url,
                data = xml,
                headers = {
                          'Content-Type': 'text/xml;charset=UTF-8',
              },
            )
        except Exception:
            pass


if __name__ == '__main__':

    obj = IacToXml()
    data = obj.get_iac_data()
    res = obj.dict_to_xml(data[0])
    print(res.decode('utf-8'))

    # res = obj.get_iac_data()
    # print(res)
