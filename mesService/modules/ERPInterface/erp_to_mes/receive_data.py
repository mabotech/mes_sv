# -*- coding: utf-8 -*-
# @createTime    : 2019/10/25 21:22
# @author  : 王江桥
# @fileName: receive_data.py
# @email: jiangqiao.wang@mabotech.com

from flask import views
from flask import Blueprint

from .item.reveive_item import IacOrder


bom = Blueprint("bom", __name__)
dev = Blueprint("dev", __name__)
ite = Blueprint("ite", __name__)


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
        iac_obj = IacOrder(status="development")
        ret = iac_obj.parse_xml()
        print(ret)

        return "200 ok "

    def post(self):
        pass


bom.add_url_rule("/bom", view_func=BomView.as_view(name="bom"))
dev.add_url_rule("/deviation", view_func=DevView.as_view(name="deviation"))
ite.add_url_rule("/item", view_func=IteView.as_view(name="item"))
