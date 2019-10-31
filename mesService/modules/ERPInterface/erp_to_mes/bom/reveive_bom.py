# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com

<<<<<<< HEAD

import json
import traceback
import xmltodict
from lxml import etree
from flask import request
from flask import current_app

from mesService.constants import BOM_ENUM
from mesService.constants import STATUS_ENUM


class BomOrder(object):
=======
from lxml import etree
import xmltodict

from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class BomOrder(object):
    def __init__(self, path=r'C:\Users\Administrator\Desktop\BFCEC\FotonEnv\interface_func\xml_to_dict\bom\text.xml', status=None):
        self.xml_path = path
        self.db = self.insertDatabase(status)
>>>>>>> fcdb3b309fd730deb9a54fb736fe9bd60e995b0c

    def parse_xml(self):
        """
        function:xml数据解析
        :return: 返回列表数据
        """
<<<<<<< HEAD
        xml_data = request.data
        xmlObj = etree.HTML(xml_data)
        xml_str = etree.tostring(xmlObj)
=======
        tree = etree.parse(self.xml_path)
        xml_str = etree.tostring(tree)
>>>>>>> fcdb3b309fd730deb9a54fb736fe9bd60e995b0c
        dict_data = self.xml_to_dict(xml_str)

        return dict_data

    def xml_to_dict(self, xml_str):
        """
        function:传入xml字符串类型数据，返回数据列表
        :param xml_str:字符串数据
        :return: 返回数据列表，列表中存放字典型数据
        """
<<<<<<< HEAD
        list_data = xmltodict.parse(xml_str)['html']['body']['bomload']['bomload']
        need_keys = ['transactionid', 'plantcode', 'header_item', 'bill_sequence_id', 'line_item',
                     'conponent_sequence_id',
                     'type', 'status', 'quantity', 'effective_date', 'disable_date']
=======
        list_data = xmltodict.parse(xml_str)['input']['BOMLOAD']['BOMLoad']
        need_keys = ['TransactionID', 'PlantCode', 'Header_Item', 'Bill_Sequence_ID', 'Line_Item',
                     'Conponent_Sequence_ID',
                     'Type', 'Status', 'Quantity', 'Effective_Date', 'Disable_Date']
>>>>>>> fcdb3b309fd730deb9a54fb736fe9bd60e995b0c

        result = []
        for p, n in dict(list_data).items():
            new_dict = {}
            if p in need_keys:
                new_dict[p] = n
<<<<<<< HEAD
            if p == "type":
                r_type = self.get_stuff_type(n)
                new_dict["type"] = r_type
            if p == "status":
                r_type = self.get_status_type(n)
                new_dict["status"] = r_type

=======
>>>>>>> fcdb3b309fd730deb9a54fb736fe9bd60e995b0c
            result.append(new_dict)

        return result

    def insertDatabase(self, dict_data):
<<<<<<< HEAD
        """调用存储过程"""
        json_data = json.dumps(dict_data)
        print(json_data)
        sql = "select product_component_insert('{}');".format(json_data)
        # print(sql)
        try:
            ret = current_app.db.query(sql)
            return ret
        except Exception as e:
            current_app.logger.error(traceback.format_exc())

    def get_status_type(self, data):
        """
        function:返回bom状态
        :param data:启用(1)或禁用(0)
        :return: 1或者0
        """
        return STATUS_ENUM[data]

    def get_stuff_type(self, data):
        """
        function:判断材料类型，例如‘{'Item_Type': 'BFCEC_采购件'}’
        :param data:
        :return:
        """
        try:
            return BOM_ENUM[data]
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
=======

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
    obj = BomOrder()
    ret = obj.parse_xml()
    print(ret)
>>>>>>> fcdb3b309fd730deb9a54fb736fe9bd60e995b0c
