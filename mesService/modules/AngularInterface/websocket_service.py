# -*- coding: utf-8 -*-
# @createTime    : 2019/12/3 11:33
# @author  : Huanglg
# @fileName: websocket_service.py
# @email: luguang.huang@mabotech.com
import json
import sys

from flask import Blueprint
from mesService.lib.redisLib.RedisHelper import RedisHelper

ws_blue = Blueprint('ws_blue', __name__, url_prefix="/ws/v1")

@ws_blue.route('/echo')
def echo(ws):
    while True:
        msg = ws.receive()
        if msg is not None:
            ws.send(msg)
        else: return

@ws_blue.route('/sub')
def sub(ws):
    obj = RedisHelper('fm104.5', 'fm104.5')
    redis_sub = obj.subscribe()

    while True:
        msg = redis_sub.parse_response()
        msg = json.dumps(msg)
        if msg is not None:
            ws.send(msg)
