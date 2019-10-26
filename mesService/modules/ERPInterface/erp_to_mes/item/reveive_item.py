# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com

import json
import xmltodict
from lxml import etree


from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class IacOrder(object):
    def __init__(self, path=r'C:\Users\Administrator\Desktop\BFCEC\foton\mesService\mesService\modules\ERPInterface\erp_to_mes\item\text.xml', status=None):
        self.xml_path = path
        self.status = status
        # self.db = self.insertDatabase(status)

    def parse_xml(self):
        """
        function:xml数据解析
        :return: 返回列表数据
        """
        print(self.xml_path)
        tree = etree.parse(self.xml_path)
        xml_str = etree.tostring(tree)
        dict_data = self.xml_to_dict(xml_str)

        return dict_data

    def xml_to_dict(self, xml_str):
        """
        function:传入xml字符串类型数据，返回数据列表
        :param xml_str:字符串数据
        :return: 返回数据列表，列表中存放字典型数据
        """
        list_data = xmltodict.parse(xml_str)['input']['ITEMLOAD']['ITEMLoad']
        need_keys = ['TransactionID', 'Item_ID', 'PlantCode', 'PartNum', 'Description', 'Item_Type', 'Status', 'UOM']

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




# if __name__ == '__main__':
#     obj = IacOrder()
#     ret = obj.parse_xml()
#     print(ret)
