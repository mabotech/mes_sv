# -*- coding: utf-8 -*-
# @createTime    : 2019/10/25 21:22
# @author  : 王江桥
# @fileName: receive_data.py
# @email: jiangqiao.wang@mabotech.com
import re
import time
import json
from lxml import etree
from flask import views
from flask import Blueprint
from flask import current_app
from flask.json import jsonify

from mesService import constants
from .item.reveive_item import ItemOrder
from .wip_order.reveive_wiporder import WipOrderInterface
from.wip_sequence.reveive_sequence import SequenceInterface

bom = Blueprint("bom", __name__, url_prefix=constants.URL_PREFIX)
dev = Blueprint("dev", __name__, url_prefix=constants.URL_PREFIX)
ite = Blueprint("ite", __name__, url_prefix=constants.URL_PREFIX)
wip = Blueprint("wip", __name__, url_prefix=constants.URL_PREFIX)
sequence = Blueprint("wip_sequence", __name__, url_prefix=constants.URL_PREFIX)



class BomView(views.MethodView):
    """
    物料(Bom)接口
    数据库：Product_Component
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        pass


class DevView(views.MethodView):
    """
    工单偏离(Deviation)接口
    数据库：Wip_Deviation
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        pass


class IteView(views.MethodView):
    """
    物料(ITEM)接口
    数据库：product
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        iac_obj = ItemOrder(status="development")
        data = iac_obj.parse_xml()
        # print(data)
        iac_obj.insertDatabase(data)

        ret = {
            'status': '200',
            'msg': 'success'
        }

        return jsonify(ret)


class WipView(views.MethodView):
    """
    工单(ITEM)接口
    数据库：postgres
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        # wiporder类
        wiporderInterface = WipOrderInterface()
        # 解析订单XML数据
        insertData = wiporderInterface.analysisFromXML()

        json_data = json.dumps(insertData)
        print(json_data)
        # 创建sql语句
        base_sql = """select plv8_insert_wiporder('{}');"""
        sql = base_sql.format(json_data)
        print(sql)
        # 调用数据库函数
        result = current_app.db.execute(sql)

        ret = {
            'status': '200',
            'msg': 'success'
        }
        return jsonify(ret)

class SequenceView(views.MethodView):
     """
     排序(ITEM)接口
     数据库：postgres
     """
     method = ["GET", "POST"]

     def get(self):
        pass

     def post(self):
         # Sequence类
         sequenceInterface = SequenceInterface()
         # 解析订单XML数据
         insertData = sequenceInterface.analysisFromXML()

         json_data = json.dumps(insertData)
         print('json_data:',json_data)
         # 创建sql语句
         base_sql = """select plv8_insert_sequence('{}');"""
         sql = base_sql.format(json_data)
         print(sql)
         # 调用数据库函数
         result = current_app.db.execute(sql)

         ret = {
             'status': '200',
             'msg': 'success'
         }
         return jsonify(json_data)

bom.add_url_rule("/bom", view_func=BomView.as_view(name="bom"))
dev.add_url_rule("/deviation", view_func=DevView.as_view(name="deviation"))
ite.add_url_rule("/item", view_func=IteView.as_view(name="item"))
wip.add_url_rule("/wip", view_func=WipView.as_view(name="wip"))
sequence.add_url_rule("/wip_sequence", view_func=SequenceView.as_view(name="wip_sequence"))
