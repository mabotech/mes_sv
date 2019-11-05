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
from flask import request
from flask import Blueprint
from flask import current_app
from flask.json import jsonify
from mesService import constants
from .wiptrx.send_wiptrx import WiptrxInterface


wiptrx = Blueprint("wiptrx", __name__, url_prefix=constants.URL_PREFIX)


class WiptrxView(views.MethodView):
    """
    wiptrx接口
    数据库：postgres
    """
    method = ["GET", "POST"]
    def get(self):
        pass

    def post(self):
        # 实例化offline类
        wiptrxInterface = WiptrxInterface()

        json_data = str(request.data, 'utf-8')

        # 创建sql语句
        base_sql = """select plv8_get_wiptrx('{}');"""

        #执行sql语句
        sql = base_sql.format(json_data)
        print(sql)
        result = current_app.db.query(sql)

        dalist = []
        sql_result=result[0].get('plv8_get_wiptrx')
        print(sql_result)
        for item in sql_result:
            offlineobj = wiptrxInterface.wiptrxDatabaseObj
            offlineobj['wiporderno'] = item['wiporderno']                             # 工单编号
            offlineobj['releasedfacility'] = item['releasedfacility']               # 工厂代码
            offlineobj['productionlineno'] = item['productionlineno']               # 产线
            offlineobj['transactiontype'] = item['transactiontype']
            offlineobj['transactionid'] = item['transactionid']
            offlineobj['serialno'] = item['serialno']
            offlineobj['currentworkcenter'] = item['currentworkcenter']

            dalist.append(offlineobj.copy())

        print(dalist)

        #生成XML
        wiptrxXml = wiptrxInterface.genOnlineXML(dalist)

        return wiptrxXml

wiptrx.add_url_rule("/wiptrx", view_func=WiptrxView.as_view(name="wiptrx"))