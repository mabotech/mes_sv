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

from mesService.constants import ACTIONS_ENUM
from mesService.modules.RabbitMQ import logger


class DeviationOrder(object):
    db = None

    def __init__(self, itype):
        self.db = create_conn(itype)

    def parse_xml(self, xml_data, xml_body):
        """
        function:解析本地xml文件,返回字典型数据
        :return:
        """
        # xmlObj = etree.parse(self.xml_path)  # 解析本地xml文件
        # xml_data = request.data
        # print(xml_data, "xml_data")
        xmlObj = etree.HTML(xml_data)  # 解析本地xml文件
        xml_str = etree.tostring(xmlObj)  # 将文件内容转换成字符串数据

        # xml_body = request.get_data(as_text=True)
        # print(xml_body, ">>>")
        dict_data = self.xml_to_dict(xml_str, xml_body)

        return dict_data

    def xml_to_dict(self, xml_str, xml_body):
        """
        function:将xml字符串转换成json字符串，获取json字符串返回字典型数据
        :param xml_str:
        :return:
        """
        list_data = xmltodict.parse(xml_str)['html']['body']['erpdev']
        need_keys = ['transactionid', 'plantcode', 'work_order_number', 'action', 'workstation', 'child_part_number',
                     'parent_part_number', 'level_1_part', 'quantity', 'manufacturing_variation_code']

        result = []
        for p, n in dict(list_data).items():
            new_dict = {}
            if p in need_keys:
                new_dict[p] = n
            # if p == "action":
            #     r_type = self.get_status_type(n)
            #     new_dict["action"] = r_type

            result.append(new_dict)

        body_dict = {"request_body": xml_body}
        result.append(body_dict)

        return result

    def insertDatabase(self, dict_data):

        """调用存储过程"""
        json_data = json.dumps(dict_data)
        # print(json_data)
        sql = "select wip_deviation_insert('{}');".format(json_data)
        # print(sql)
        try:
            # 使用execute返回存储过程返回结果，存储过程不报错则返回1
            # 使用query返回查询结果，通过结果做判断
            # with self.app.app_context():
            ret = self.db.query(sql)
            return ret
        except Exception:
            # with self.app.app_context():
            #     current_app.logger.error(traceback.format_exc())
            logger.writeLog("数据库写入失败:" + sql, os.path.basename(os.path.dirname(os.getcwd())) + ".log")

    def get_status_type(self, data):
        """
        function:返回偏离类型
        :param data:增加(A)或者删除(D)
        :return: 1或者0
        """
        return ACTIONS_ENUM[data]
