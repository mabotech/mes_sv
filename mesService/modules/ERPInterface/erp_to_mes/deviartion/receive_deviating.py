# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com
import json

from lxml import etree
import xmltodict


from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class DeviationOrder(object):

    def __init__(self, path=r'C:\Users\Administrator\Desktop\BFCEC\FotonEnv\interface_func\xml_to_dict\deviartion(工单偏离)\text.xml', status=None):
        self.xml_path = path
        self.db = self.create_conn(status)

    def parse_xml(self):
        """
        function:解析本地xml文件,返回字典型数据
        :return:
        """
        xmlObj = etree.parse(self.xml_path)  # 解析本地xml文件
        xml_str = etree.tostring(xmlObj)  # 将文件内容转换成字符串数据
        dict_data = self.xml_to_dict(xml_str)
        return dict_data

    def xml_to_dict(self, xml_str):
        """
        function:将xml字符串转换成json字符串，获取json字符串返回字典型数据
        :param xml_str:
        :return:
        """
        list_data = xmltodict.parse(xml_str)['input']['ERPDEV']  # 将xml文件转换成json数据类型
        need_keys = ['TransactionID', 'PlantCode', 'Work_Order_Number', 'Action', 'Workstation', 'Child_Part_Number',
                     'Parent_Part_Number', 'Level_1_Part', 'Quantity', 'Manufacturing_Variation_Code']

        result = []
        for p, n in dict(list_data).items():
            new_dict = {}
            if p in need_keys:
                new_dict[p] = n
            result.append(new_dict)

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
    obj = DeviationOrder("development")
    res = obj.parse_xml()
    # obj.insertDatabase(res)
    print(res)
