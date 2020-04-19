# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com

import os
import json
import xmltodict
import traceback
from lxml import etree
from flask import request
from flask import current_app
from mesService import create_conn

from mesService.modules.RabbitMQ import logger
from mesService.constants import STATUS_ENUM
from mesService.constants import PRODUCTINVENTORYTYPE_ENUM


class ItemOrder(object):
    db = None

    def __init__(self, itype):
        self.db = create_conn(itype)

    def parse_xml(self, xml_str, xml_body):
        """
        function:xml数据解析
        :return: 返回列表数据
        """
        # xml_str = request.data
        tree = etree.HTML(xml_str)
        xml_str = etree.tostring(tree)

        # xml_body = request.get_data(as_text=True)
        # print(xml_body, ">>>")
        dict_data = self.xml_to_dict(xml_str, xml_body)

        return dict_data

    def xml_to_dict(self, xml_str, xml_body):
        """
        function:传入xml字符串类型数据，返回数据列表
        :param xml_str:字符串数据
        :return: 返回数据列表，列表中存放字典型数据
        """
        # list_data = xmltodict.parse(xml_str)['input']['ITEMLOAD']['ITEMLoad']
        print("xml_str",xml_str)
        list_data = xmltodict.parse(xml_str)['html']['body']['sendsuppliercurrentaccountservicebal']['data']['itemload']['itemload']
        print("list_data",list_data)
        need_keys = ['transactionid', 'item_id', 'plantcode', 'partnum', 'description', 'item_type', 'status', 'uom']

        result = []
        for p, n in dict(list_data).items():
            new_dict = {}
            if p in need_keys:
                new_dict[p] = n
                if p == "item_type":
                    r_type = self.get_stuff_type(n)
                    new_dict["item_type_val"] = r_type
                if p == "status":
                    r_type = self.get_status_type(n)
                    new_dict["status"] = r_type

            result.append(new_dict)

        language_dict = {'language': 2052}
        body_dict = {"request_body": xml_body}
        result.append(body_dict)
        result.append(language_dict)

        return result

    def get_stuff_type(self, data):
        """
        function:判断材料类型，例如‘{'Item_Type': 'BFCEC_采购件'}’
        :param data:
        :return:
        """
        try:
            return PRODUCTINVENTORYTYPE_ENUM[data]
        except Exception:
            return PRODUCTINVENTORYTYPE_ENUM['BFCEC_通用类型']

    def get_status_type(self, data):
        """
        function:获取物料状态
        :return:
        """
        try:
            return STATUS_ENUM[data]
        except Exception:
            current_app.logger.error(traceback.format_exc())

    def insertDatabase(self, dict_data):

        """调用存储过程"""
        json_data = json.dumps(dict_data)
        # print(json_data)
        sql = "select item_insert('{}');".format(json_data)
        # print(sql)
        try:
            # with self.app.app_context():
            ret = self.db.query(sql)
            return ret
        except Exception:
            # current_app.logger.error(traceback.format_exc())
            logger.writeLog("数据库写入失败:" + sql, os.path.basename(os.path.dirname(os.getcwd())) + ".log")

