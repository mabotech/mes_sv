# -*- coding: utf-8 -*-
# @createTime    : 2019/10/25 21:22
# @author  : 王江桥
# @fileName: receive_data.py
# @email: jiangqiao.wang@mabotech.com
import random
import re
import time
import json
from lxml import etree
from flask import views
from flask import Blueprint
from flask import current_app
from flask.json import jsonify

from mesService import constants
from mesService.constants import RET
from .bom.reveive_bom import BomOrder
from .item.reveive_item import ItemOrder
from .deviartion.receive_deviating import DeviationOrder
from .wip_order.reveive_wiporder import WipOrderInterface
from .wip_sequence.reveive_sequence import SequenceInterface

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
        obj = BomOrder()
        data = obj.parse_xml()
        ret = obj.insertDatabase(data)
        # print(ret)

        c_flag = ret[0]["product_component_insert"]["component"]
        pc_flag = ret[0]["product_component_insert"]["product_component"]

        if c_flag and pc_flag:
            return jsonify(RET)
        else:
            RET['status'] = 300
            RET['msg'] = 'fail'

            return jsonify(RET)


class DevView(views.MethodView):
    """
    工单偏离(Deviation)接口
    数据库：Wip_Deviation
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        obj = DeviationOrder()
        data = obj.parse_xml()
        ret = obj.insertDatabase(data)
        print(ret, ">>>")

        if not ret:
            RET['status'] = 300
            RET['msg'] = 'fail'

        return jsonify(RET)


class IteView(views.MethodView):
    """
    物料(ITEM)接口
    数据库：product
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        iac_obj = ItemOrder()
        data = iac_obj.parse_xml()
        # print(data)
        ret = iac_obj.insertDatabase(data)

        if not ret:
            RET['status'] = 300
            RET['msg'] = 'fail'

        return jsonify(RET)


class IteView1(views.MethodView):
    """
    物料(ITEM)接口
    数据库：product
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        iac_obj = ItemOrder(status="development")
        data = [{'transactionid': 'ITEMLOAD'}, {'item_id': '4314314'}, {'plantcode': 'ISG'}, {'partnum': '3940123'}, {'description': '气阀锁块11'}, {'item_type': 'BFCEC_采购件', 'item_type_val': 100}, {'status': 1}, {'uom': 'EA'}, {'language': 2052}]
        data[3]['partnum'] = str(hash(time.time())) + str(random.randint(1,100))
        print(data)
        # print(data)
        ret = iac_obj.insertDatabase(data)

        if not ret:
            RET['status'] = 300
            RET['msg'] = 'fail'

        return jsonify(RET)


class WipView(views.MethodView):
    """
    工单(Wip_Order)接口
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
    排序(Wip_Sequence)接口
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
        print('json_data:', json_data)
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
ite.add_url_rule("/item1", view_func=IteView1.as_view(name="item1"))
wip.add_url_rule("/wip", view_func=WipView.as_view(name="wip"))
sequence.add_url_rule("/wip_sequence", view_func=SequenceView.as_view(name="wip_sequence"))