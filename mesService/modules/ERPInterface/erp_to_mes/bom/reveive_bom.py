# -*- coding: utf-8 -*-
# @createTime    : 2019/10/24 11:03
# @author  : 王江桥
# @fileName: send_bom.py
# @email: jiangqiao.wang@mabotech.com


import os
import json
import traceback
import xmltodict
from lxml import etree
from flask import request
from flask import current_app
from mesService import create_conn
from mesService.modules.RabbitMQ import logger

from mesService.constants import BOM_ENUM
from mesService.constants import STATUS_ENUM


class BomOrder(object):
    db = None

    def __init__(self, itype):
        self.db = create_conn(itype)

    def parse_xml(self, xml_data, xml_body):
        """
        function:xml数据解析
        :return: 返回列表数据
        """
        # xml_data = request.data
        try:
            xml_data = str(xml_data, encoding='utf-8')
            xmlObj = etree.HTML(xml_data)
            xml_str = etree.tostring(xmlObj)

            # xml_body = request.get_data(as_text=True)
            # print(xml_body, ">>>")
            dict_data = self.xml_to_dict(xml_str, xml_body)

            return dict_data
        except:
            result = {
                "status": "error",
                "message": "解析失败,报文格式不正确"
            }
            return json.dumps(result)
    def xml_to_dict(self, xml_str, xml_body):
        """
        function:传入xml字符串类型数据，返回数据列表
        :param xml_str:字符串数据
        :return: 返回数据列表，列表中存放字典型数据
        """
        try:
            list_data = xmltodict.parse(xml_str)['html']['body']['data']['bomload']['bomload']
            need_keys = ['transactionid', 'plantcode', 'header_item', 'bill_sequence_id', 'line_item',
                         'conponent_sequence_id',
                         'type', 'status', 'quantity', 'effective_date', 'disable_date']

            result = []
            print(list_data)
            for p, n in dict(list_data).items():
                new_dict = {}
                if p in need_keys:
                    new_dict[p] = n
                if p == "type":
                    r_type = self.get_stuff_type(n)
                    new_dict["type"] = r_type
                if p == "status":
                    r_type = self.get_status_type(n)
                    new_dict["status"] = r_type

                result.append(new_dict)
            # 报文原始数据
            body_dict = {"request_body": xml_body}
            """
            USAGE_TYPE:
                BOM: 1
                IAC工位BOM: 2
                工单偏离: 3
                实时偏离: 4
            """
            usagetype_dict = {"usagetype": 1}
            result.append(body_dict)
            result.append(usagetype_dict)

            return result
        except:
            result = {
                "status": "error",
                "message": "解析失败,报文格式不正确"
            }
            return json.dumps(result)

    def insertDatabase(self, dict_data):
        """调用存储过程"""
        json_data = json.dumps(dict_data)
        # print(json_data)
        sql = "select product_component_insert('{}');".format(json_data)
        print(sql)
        try:
            # with self.app.app_context():
            ret = self.db.query(sql)
            return ret
        except Exception as e:
            # current_app.logger.error(traceback.format_exc())
            logger.writeLog("数据库写入失败:" + sql, os.path.basename(os.path.dirname(os.getcwd())) + ".log")

    def get_status_type(self, data):
        """
        function:返回bom状态
        :param data:启用(1)或禁用(0)
        :return: 1或者0
        """
        try:
            return STATUS_ENUM[data]
        except Exception:
            current_app.logger.error(traceback.format_exc())

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
