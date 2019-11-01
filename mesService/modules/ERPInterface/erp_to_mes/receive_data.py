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
sequence = Blueprint("sequence", __name__, url_prefix=constants.URL_PREFIX)


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

        c_flag = ret[0]["product_component_insert"].get("component_result", None)
        p_err = ret[0]["product_component_insert"].get("component_result_e", None)
        pc_flag = ret[0]["product_component_insert"].get("product_component_result", None)
        pc_err = ret[0]["product_component_insert"].get("product_component_result_e", None)
        lii_inv = ret[0]["product_component_insert"].get("component_line_item_id_invalid", None)
        hii_inv = ret[0]["product_component_insert"].get("product_component_header_item_id_invalid", None)

        if c_flag and pc_flag:
            RET['status'] = 200
            RET['msg'] = 'insert success'
        elif p_err or pc_err:
            RET['status'] = 300
            RET['msg'] = "{0}或者{1}错误！".format(p_err, pc_err)
        elif lii_inv:
            RET['status'] = 300
            RET['msg'] = lii_inv
        elif hii_inv:
            RET['status'] = 300
            RET['msg'] = hii_inv

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

        iwd_flag = ret[0]["wip_deviation_insert"].get("insert_wipdeviation", None)
        iwd_err = ret[0]["wip_deviation_insert"].get("insert_wipdeviation_e", None)
        iwd_inv = ret[0]["wip_deviation_insert"].get("insert_wipdeviation_invalid", None)

        if iwd_flag:
            RET['status'] = 200
            RET['msg'] = 'insert success'
        elif iwd_err:
            RET['status'] = 300
            RET['msg'] = iwd_err
        else:
            RET['status'] = 300
            RET['msg'] = iwd_inv

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
        print(ret, "<<<")
        ip_flag = ret[0]["item_insert"].get("insert_product", None)
        up_flag = ret[0]["item_insert"].get("update_product", None)
        ip_err = ret[0]["item_insert"].get("insert_product_e", None)
        up_err = ret[0]["item_insert"].get("update_product_e", None)

        if ip_flag:
            RET['status'] = 200
            RET['msg'] = 'insert success'
        elif up_flag:
            RET['status'] = 200
            RET['msg'] = 'update success'
        elif ip_err:
            RET['status'] = 300
            RET['msg'] = ip_err
        elif up_err:
            RET['status'] = 300
            RET['msg'] = up_err

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
        iac_obj = ItemOrder()
        data = [{'transactionid': 'ITEMLOAD'}, {'item_id': '4314314'}, {'plantcode': 'ISG'}, {'partnum': '3940123'},
                {'description': '气阀锁块11'}, {'item_type': 'BFCEC_采购件', 'item_type_val': 100}, {'status': 1},
                {'uom': 'EA'}, {'language': 2052}]
        data[3]['partnum'] = str(hash(time.time())) + str(random.randint(1, 100))
        print(data)
        # print(data)
        ret = iac_obj.insertDatabase(data)

        if not ret:
            RET['status'] = 300
            RET['msg'] = 'fail'

        return jsonify(RET)


class WipView(views.MethodView):
    """
    工单(WipOrder)接口
    数据库：postgres
    """
    method = ["GET", "POST"]

    def get(self):
        result = {
            "status": "error",
            "message": "illegal request"
        }
        res = json.dumps(result)
        return res

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
        result = current_app.db.query(sql)
        sql_result = result[0].get('plv8_insert_wiporder')
        print(sql_result)

        return jsonify(sql_result)


class SequenceView(views.MethodView):
    """
    排序(Wip_Sequence)接口
    数据库：postgres
    """
    method = ["GET", "POST"]

    def get(self):
        result = {
            "status": "error",
            "message": "illegal request"
        }
        res = json.dumps(result)
        return res

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
        result = current_app.db.query(sql)
        sql_result = result[0].get('plv8_insert_sequence')
        print('result',sql_result)

        return jsonify(sql_result)


bom.add_url_rule("/bom", view_func=BomView.as_view(name="bom"))
dev.add_url_rule("/deviation", view_func=DevView.as_view(name="deviation"))
ite.add_url_rule("/item", view_func=IteView.as_view(name="item"))
wip.add_url_rule("/wiporder", view_func=WipView.as_view(name="wip_order"))
sequence.add_url_rule("/wipsequence", view_func=SequenceView.as_view(name="wip_sequence"))
