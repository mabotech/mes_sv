# -*- coding: utf-8 -*-
# @createTime    : 2019/10/31 14:05
# @author  : 王江桥
# @fileName: send_cbo.py
# @email: jiangqiao.wang@mabotech.com

import traceback
from lxml import etree
from flask import current_app
from mesService.config import config_dict
from mesService.lib.pgwrap.db import connection


class CboToXml(object):
    def __init__(self):
        self.root = etree.Element('root')
        # self.db = self.create_conn('development')

    def dict_to_xml(self, dict_data):
        """
        function:字典型数据转换成XML数据
        :param dict_data: {k1:v1, k2:v2...}
        :return: XML文件
        """
        for k, v in dict_data.items():
            item = etree.SubElement(self.root, 'item')
            try:
                item.set('name', k)
                item.set('value', v)
            except Exception as e:
                current_app.logger.error(traceback.format_exc())

        print(etree.tostring(self.root, pretty_print=True))

        tree = etree.ElementTree(self.root)
        tree.write('text.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')

    def queryDatanase(self):
        """
        function:执行sql获取查询数据
        :return: [{k1:v1},{k2:v2}...]
        """
        sql = "select get_cbo()"
        # print(sql)
        try:
            # ret = self.db.query(sql)
            ret = current_app.db.query(sql)
            return ret[0]['get_cbo'].get("rec_data", None)
        except Exception as e:
            current_app.logger.error(traceback.format_exc())

    def parse_data(self, re_data):
        """
        function:循环获取单条数据，每条数据调用dict_to_xml生成XML文件
        :param re_data:
        :return:
        """
        if re_data:
            for data in re_data:
                self.dict_to_xml(data)
        else:
            current_app.logger.info("当前记录不存在")

    def create_conn(self, config_name):
        """
        function:创建db测试连接
        :param config_name:
        :return:
        """
        conn = config_dict[config_name].DB_INFO
        db = connection(conn)
        return db


if __name__ == '__main__':
    obj = CboToXml()
    data = obj.queryDatanase()
    obj.parse_data(data)
