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
from .offline.send_offline import OfflineInterface


offline = Blueprint("offline", __name__, url_prefix=constants.URL_PREFIX)


class OfflineView(views.MethodView):
    """
    完工(offline)接口
    数据库：postgres
    """
    method = ["GET", "POST"]
    def get(self):
        # 实例化offline类
        offlineInterface = OfflineInterface()

        # 创建sql语句
        base_sql = """select plv8_get_offline('{}');"""

        #执行sql语句
        sql = base_sql.format('SO12555000104')
        print(sql)
        result = current_app.db.query(sql)

        dalist = []
        sql_result=result[0].get('plv8_get_offline')
        for item in sql_result:
            offlineobj = offlineInterface.offlineDatabaseObj
            offlineobj['wiporderno'] = item['wiporderno']
            offlineobj['wiporderno'] = item['wiporderno']  # 工单编号
            offlineobj['releasedfacility'] = item['releasedfacility']   # 工厂代码
            offlineobj['productionlineno'] = item['productionlineno'] # 产线
            dalist.append(offlineobj.copy())

        print(dalist)

        #生成XML
        OffXml = offlineInterface.genOnlineXML(dalist)

        return OffXml


offline.add_url_rule("/offline", view_func=OfflineView.as_view(name="offline"))