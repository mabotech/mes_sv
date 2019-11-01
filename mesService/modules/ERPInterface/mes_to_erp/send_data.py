# -*- coding: utf-8 -*-
# @createTime    : 2019/10/25 21:23
# @author  : 王江桥
# @fileName: send_data.py
# @email: jiangqiao.wang@mabotech.com

import re
import time
import json
from lxml import etree
from flask import views
from mesService import constants
from flask import Blueprint
from flask import current_app
from flask.json import jsonify
from .wiptrx.send_wiptrx import WiptrxInterface


wiptrx = Blueprint("wiptrx", __name__, url_prefix=constants.URL_PREFIX)


class WiptrxView(views.MethodView):
    """
    完工(wiptrx)接口
    数据库：postgres
    """
    method = ["GET", "POST"]
    def get(self):
        pass

    def post(self):
        # 实例化offline类
        wiptrxInterface = WiptrxInterface()

        # 创建sql语句
        base_sql = """select plv8_get_wiptrx('{}','{}','{}');"""

        #执行sql语句
        sql = base_sql.format('SO12555000104','ISF','ENGSTATUS')
        print(sql)
        result = current_app.db.query(sql)

        dalist = []
        sql_result=result[0].get('plv8_get_wiptrx')
        for item in sql_result:
            offlineobj = wiptrxInterface.wiptrxDatabaseObj
            offlineobj['wiporderno'] = item['wiporderno']  # 工单编号
            offlineobj['releasedfacility'] = item['releasedfacility']   # 工厂代码
            offlineobj['productionlineno'] = item['productionlineno'] # 产线
            dalist.append(offlineobj.copy())

        print(dalist)

        #生成XML
        wiptrxXml = wiptrxInterface.genOnlineXML(dalist)

        return wiptrxXml

wiptrx.add_url_rule("/wiptrx", view_func=WiptrxView.as_view(name="wiptrx"))