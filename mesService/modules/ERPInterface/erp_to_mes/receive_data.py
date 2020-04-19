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
from flask import request
from flask import Blueprint
from flask import current_app
from flask.json import jsonify

from mesService import constants
from mesService.constants import RET
# from .bom.reveive_bom import BomOrder
# from .item.reveive_item import ItemOrder
from mesService.config import INTERFACE_CLASS_NAME
# from .deviartion.receive_deviating import DeviationOrder
# from .wip_order.reveive_wiporder import WipOrderInterface
# from .wip_sequence.reveive_sequence import SequenceInterface
from mesService.modules.RabbitMQ.interface_pro import InterfaceRpcClient

bom = Blueprint("bom", __name__, url_prefix=constants.URL_PREFIX)
dev = Blueprint("dev", __name__, url_prefix=constants.URL_PREFIX)
ite = Blueprint("ite", __name__, url_prefix=constants.URL_PREFIX)
wip = Blueprint("wip", __name__, url_prefix=constants.URL_PREFIX)
sequence = Blueprint("sequence", __name__, url_prefix=constants.URL_PREFIX)


class BaseUtil(object):
    """
    基础类：
        1.获取请求XML数据
        2.实例化RabbitMQ的RPC-Client函数
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def interface_obj():
        url = request.base_url
        xml_data = request.data
        xml_body = request.get_data(as_text=True)
        classname = INTERFACE_CLASS_NAME[f"{url}"]
        param = {}
        param["classname"] = classname
        param["xml_data"] = bytes.decode(xml_data,'utf-8')
        param["xml_body"] = xml_body
        param_dict = json.dumps(param)
        obj = InterfaceRpcClient()

        return param_dict, obj


class BomView(BaseUtil, views.MethodView):
    """
    物料(Bom)接口
    数据库：Product_Component
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        # obj = BomOrder()
        # data = obj.parse_xml()
        # ret = obj.insertDatabase(data)
        # print(ret)
        param_dict, obj = super().interface_obj()
        try:
            ret = obj.call(param_dict)
        except:
            # 再次放入队列
            ret = obj.call(param_dict)
        self.parse_data(ret)

        return jsonify(RET)

    def parse_data(self, ret):
        c_flag = ret[0]["product_component_insert"].get("component_result", None)
        c_err = ret[0]["product_component_insert"].get("component_result_e", None)
        cup_flag = ret[0]["product_component_insert"].get("component_result_up", None)
        cup_err = ret[0]["product_component_insert"].get("component_result_upe", None)
        pcup_flag = ret[0]["product_component_insert"].get("product_component_result_up", None)
        pcup_err = ret[0]["product_component_insert"].get("product_component_result_upe", None)
        pc_flag = ret[0]["product_component_insert"].get("product_component_result", None)
        pc_err = ret[0]["product_component_insert"].get("product_component_result_e", None)
        lii_inv = ret[0]["product_component_insert"].get("component_line_item_id_invalid", None)
        hii_inv = ret[0]["product_component_insert"].get("product_component_header_item_id_invalid", None)

        if c_flag or pc_flag or cup_flag or pcup_flag:
            RET['status'] = 200
            RET['msg'] = 'execute success'
        elif c_err or cup_err or pc_err or pcup_err:
            RET['status'] = 300
            RET['msg'] = "{0}/{1}/{2}/{3}错误！".format(c_err, cup_err, pc_err, pcup_err)
        elif lii_inv:
            RET['status'] = 300
            RET['msg'] = lii_inv
        elif hii_inv:
            RET['status'] = 300
            RET['msg'] = hii_inv
        else:
            RET['status'] = 400
            RET['msg'] = "未知错误！"


class DevView(BaseUtil, views.MethodView):
    """
    工单偏离(Deviation)接口
    数据库：Wip_Deviation
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        # obj = DeviationOrder()
        # data = obj.parse_xml()
        # ret = obj.insertDatabase(data)
        param_dict, obj = super().interface_obj()
        try:
            ret = obj.call(param_dict)
        except:
            # 再次放入队列
            ret = obj.call(param_dict)
        self.parse_data(ret)

        return jsonify(RET)

    def parse_data(self, ret):
        iwd_flag = ret[0]["wip_deviation_insert"].get("insert_wipdeviation", None)
        iwd_err = ret[0]["wip_deviation_insert"].get("insert_wipdeviation_e", None)
        dwd_flag = ret[0]["wip_deviation_insert"].get("update_wipdeviation", None)
        dwd_err = ret[0]["wip_deviation_insert"].get("update_wipdeviation_e", None)
        iwd_inv = ret[0]["wip_deviation_insert"].get("insert_wipdeviation_invalid", None)
        plantcode = ret[0]["wip_deviation_insert"].get("plantcode", None)

        if iwd_flag:
            RET['status'] = 200
            RET['msg'] = 'insert success'
        elif dwd_flag:
            RET['status'] = 200
            RET['msg'] = 'delete success'
        elif iwd_err or dwd_err:
            RET['status'] = 300
            RET['msg'] = "{0}或者{1}报错".format(iwd_err, dwd_err)
        elif iwd_inv:
            RET['status'] = 300
            RET['msg'] = iwd_inv
        elif plantcode:
            RET['status'] = 300
            RET['msg'] = plantcode
        else:
            RET['status'] = 400
            RET['msg'] = "其他错误信息！"


class IteView(BaseUtil, views.MethodView):
    """
    物料(ITEM)接口
    数据库：product
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        # iac_obj = ItemOrder()
        # data = iac_obj.parse_xml()
        # print(data)
        # ret = iac_obj.insertDatabase(data)
        # print(ret, "<<<")
        param_dict, obj = super().interface_obj()
        try:
            ret = obj.call(param_dict)
        except:
            # 再次放入队列
            ret = obj.call(param_dict)
        self.parse_data(ret)

        return jsonify(RET)

    def parse_data(self, ret):
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
        else:
            RET['status'] = 400
            RET['msg'] = "未知错误！"


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


class WipView(BaseUtil,views.MethodView):
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
        param_dict, obj = super().interface_obj()

        retry_flag = False
        try:
            ret = obj.call(param_dict)
        except:
            # 再次放入队列
            ret = obj.call(param_dict)

        return jsonify(ret)


class SequenceView(BaseUtil,views.MethodView):
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
        param_dict, obj = super().interface_obj()

        retry_flag = False
        try:
            ret = obj.call(param_dict)
        except:
            # 再次放入队列
            ret = obj.call(param_dict)

        return jsonify(ret)


bom.add_url_rule("/bom", view_func=BomView.as_view(name="bom"))
dev.add_url_rule("/deviation", view_func=DevView.as_view(name="deviation"))
ite.add_url_rule("/item", view_func=IteView.as_view(name="item"))
wip.add_url_rule("/wiporder", view_func=WipView.as_view(name="wip_order"))
sequence.add_url_rule("/wipsequence", view_func=SequenceView.as_view(name="wip_sequence"))
