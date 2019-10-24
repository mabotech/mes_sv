# -*- coding: utf-8 -*-
# @createTime    : 2019/10/10 10:04
# @author  : Huanglg
# @fileName: receive_deviating.py
# @email: luguang.huang@mabotech.com
import json

from lxml import etree
import xmltodict

from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class deviationOrder(object):

    def __init__(self, path = r'F:\BeijingMES\mesInterface\deviation_order.xml'):
        self.xml_path = path
        self.db = self.create_conn('development')

    def parse_xml(self):

        xmlObj = etree.parse(self.xml_path)
        xml_str = etree.tostring(xmlObj)
        dict_data = self.xml_to_dict(xml_str)
        return dict_data

    def xml_to_dict(self, xml_str):

        list_data = xmltodict.parse(xml_str)['input']['ERPDEV']
        need_keys = ['Work_Order_Number', 'Action', 'Workstation', 'Child_Part_Number', 'Parent_Part_Number',
                     'Level_1_Part', 'Quantity', 'Manufacturing_Variation_Code']
        result = []
        for d in list_data:
            temp_d = {}
            for k, v in d.items():
                if k in need_keys:
                    temp_d[k] = v
            result.append(temp_d)
        return result

    def insertDatabase(self, dict_data):

        """调用存储过程"""
        json_data = json.dumps(dict_data)
        sql = "select insert_deviate_orders('{}');".format(json_data)
        print(sql)
        try:
            self.db.execute(sql)
        except Exception as e:
            pass


    def create_conn(self, config_name):
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

if __name__ == '__main__':
    # get_deviation_xml()
    obj = deviationOrder()
    res = obj.parse_xml()
    obj.insertDatabase(res)
    print(res)
