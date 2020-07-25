# -*- coding: utf-8 -*-
# @createTime    : 2019/10/25 21:23
# @author  : 王江桥
# @fileName: send_data.py
# @email: jiangqiao.wang@mabotech.com

import re
import time
import json
import requests
import xmltodict
from lxml import etree
from flask import views
from flask import request
from flask import Blueprint
from flask import current_app
from flask.json import jsonify
from mesService import constants
from mesService.constants import RET
from mesService.modules.ERPInterface.mes_to_erp.cbo.send_cbo import CboToXml
from .wiptrx.send_wiptrx import WiptrxInterface


wiptrx = Blueprint("wiptrx", __name__, url_prefix=constants.URL_PREFIX)
cbo = Blueprint("cbo", __name__, url_prefix=constants.URL_PREFIX)


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
        print(json_data)

        # 创建sql语句
        base_sql = """select plv8_get_wiptrx('{}');"""

        # 执行sql语句
        sql = base_sql.format(json_data)
        print("执行sql语句", sql)
        result = current_app.db.query(sql)

        dalist = []
        sql_result = result[0].get('plv8_get_wiptrx')
        print("返回结果：",sql_result)
        if 'error' in sql_result:
            return jsonify(sql_result)
        for item in sql_result:
            offlineobj = wiptrxInterface.wiptrxDatabaseObj
            offlineobj['wiporderno'] = item['wiporderno']  # 工单编号
            offlineobj['releasedfacility'] = item['releasedfacility']  # 工厂代码
            offlineobj['productionlineno'] = item['productionlineno']  # 产线
            offlineobj['transactiontype'] = item['transactiontype']
            offlineobj['transactionid'] = item['transactionid']
            offlineobj['serialno'] = item['serialno']
            offlineobj['currentworkcenter'] = item['currentworkcenter']
            offlineobj['workorderstatus'] = item['workorderstatus']
            offlineobj['workcenter'] = item['workcenter']

            dalist.append(offlineobj.copy())

        # 生成XML
        wiptrxXml,data = wiptrxInterface.genOnlineXML(dalist)
        request_res = 'success'
        # result = {"result": "success", "message": None}
        # reqobj = requests.Session()
        # reqobj.auth = ('MSFM', 'MSFM202004210945')

        try:
            # request_res = reqobj.post(constants.ERP_HOST, wiptrxXml)
            # result['message'] = request_res.text

            #捕获ERP回馈信息
            # s = request_res.content
            # tree = etree.HTML(s)
            # xml_str1 = etree.tostring(tree)
            # list_data = xmltodict.parse(xml_str1)['html']['body']['envelope']['body'][
            #     'getmsfm_bfcec_052_sendmachiningordertransresponse']['sign'][1]['outputparameters']['x_status_code']
            # print('list_data', list_data)
            # if list_data == 'S':
            message = {'application': 'MES',
                       'transactionid': data['TRANSACTIONID'],
                       'transactiontype': data['TRANSACTIONTYPE'],
                       'message': '待回冲',
                       'actionstatus': '插入',
                       'wiporder': data['WIPJOBNO'],
                       'result': 0,
                       'context': wiptrxXml,
                       'createdby': ''
                       }
            json_message = json.dumps(message)
            base_sql = """select insert_outflow_log('{}');"""
            sql = base_sql.format(json_message)
            print('S',sql)
            result = current_app.db.query(sql)

        except Exception as e:
            result['result'] = 'fail'
            result['message'] = e.args

        # request_status = request_res.status_code
        # print(request_status)

        # if (request_status != 200):
        #     result['result'] = 'fail'
        #     result['message'] = '传输失败，网络不通'
        return jsonify(result)

class CBOView(views.MethodView):
    """
    CBO接口
    数据库：postgres
    """
    method = ["GET", "POST"]

    def get(self):
        pass

    def post(self):
        try:
            # 实例化offline类
            cbo = CboToXml()

            json_data = str(request.data, 'utf-8')

            # 创建sql语句
            base_sql = """select get_cbo('{}');"""

            # 执行sql语句
            sql = base_sql.format(json_data)
            print("执行sql语句", sql)
            ret = current_app.db.query(sql)
            dataset = ret[0]['get_cbo'].get("rec_data", None)
            s = []
            for data in dataset:
                # 将字段转换为对应的XML字段
                bindDatabase = cbo.bindDatabase2Xml(data)
                # 将XML字段转化为树形结构
                new = cbo.genOnlineXML(bindDatabase)
                #将所有数据存入一个列表
                s.append(new)
            tempres = "".join(s)
            #将列表放入发送报文中
            new_xml = cbo.format_soa_xml(tempres)

            print("new_xml",new_xml)
            request_res = None
            result = {"result": "success", "message": None}
            reqobj = requests.Session()
            reqobj.auth = ('MSFM', 'MSFM202004210945')
            reqobj.headers = {'Content-Type':'application/xml'}
            try:
                request_res = reqobj.post(constants.CBO_HOST, new_xml)
                print(request_res)
                result['message'] = request_res.text

            except Exception as e:
                result['result'] = 'fail'
                result['message'] = e.args
            request_status = request_res.status_code
            print(request_status)
            if (request_status != 200):
                result['result'] = 'fail'
                result['message'] = '传输失败，网络不通'

            return jsonify(result)

        except Exception as e:
            return jsonify(e)

wiptrx.add_url_rule("/wiptrx", view_func=WiptrxView.as_view(name="wiptrx"))
cbo.add_url_rule("/cbo", view_func=CBOView.as_view(name="cbo"))

