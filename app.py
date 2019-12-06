# -*- coding: utf-8 -*-
# @createTime    : 2019/8/27 14:20
# @author  : Huanglg
# @fileName: manage.py
# @email: luguang.huang@mabotech.com
import json

from mesService import create_app
from flask_jsonrpc import JSONRPC
from flask_uwsgi_websocket import GeventWebSocket
from flask_uwsgi_websocket import WebSocket
from flask import request

from mesService.lib.redisLib.RedisHelper import RedisHelper
from mesService.modules.AngularInterface.websocket_service import ws_blue

app = create_app('development')
ws = WebSocket(app)
ws.register_blueprint(ws_blue)

#jsonrpc
jsonrpc = JSONRPC(app, '/rpc/v1')
# 实现rpc接口

@app.after_request
def after_request(response):
    """
    Post request processing - add CORS, cache control headers
    """
    # Enable CORS requests for local development
    # The following will allow the local angular-cli development environment to
    # make requests to this server (otherwise, you will get 403s due to same-
    # origin poly)
    response.headers.add('Access-Control-Allow-Origin',
                         "*")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,Set-Cookie,Cookie,Cache-Control,Pragma,Expires')  # noqa
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE')

    # disable caching all requests
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    return response


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, threads=16, host='0.0.0.0')
