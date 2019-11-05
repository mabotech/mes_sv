# @createTime    : 2019/11/05 15:13
# @author  : Mou
# @fileName: callrpc.py
from flask import Blueprint
from app import jsonrpc
from flask import current_app
from mesService.lib.pgwrap.db import connection
import json


mod = Blueprint('callrpc', __name__)
jsonrpc.register_blueprint(mod)

@jsonrpc.method('callrpc(table=String, context=Object, method=String, columns=Object, pkey=String) -> Object')
def callrpc(table, context, method, columns, pkey):
        #解析请求转为PG的select语句
        sqlstr = "SELECT {0}('[{1}]') ".format(method, json.dumps(columns))
        result = current_app.db.query_one(sqlstr)
        return result