# -*- coding: utf-8 -*-
# @createTime    : 2019/8/27 14:13
# @author  : Huanglg
# @fileName: views.py
# @email: luguang.huang@mabotech.com
import json
import socket
import traceback

from . import auth_blue
from flask.json import jsonify
from mesService import constants
from flask import current_app, request, make_response, abort
from .auth import (authenticate_user, AuthenticationError, auth_required, get_authenticated_user)


@auth_blue.route('/getip')
def getip():
    try:
        ip = request.remote_addr
        return make_response(jsonify({"clientip":ip}))
    except:
        abort(404)


@auth_blue.route('/auth/login', methods=['POST'])
def login_api():
    """
    Login user
    """
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        access_token, refresh_token = authenticate_user(username, password)
        return make_response(jsonify({
            'accessToken': access_token,
            'refreshToken': refresh_token
        }))
    except AuthenticationError as error:
        current_app.logger.error('authentication error: %s', error)
        abort(403)


@auth_blue.route('/auth/info', methods=['GET', 'POST'])
@auth_required
def login_info_api():
    """
    Get informaiton about currently logged in user
    """
    try:
        user = get_authenticated_user()

        data_list = None
        sql_base = "select get_employee_all('{0}')"
        loginname = json.dumps({"loginname": user})
        sql_str = sql_base.format(loginname)
        try:
            employee_info = current_app.db.query(sql_str)
            data_list = employee_info[0]["get_employee_all"]
        except Exception:
            current_app.logger.error(traceback.format_exc())

        # 获取所有员工信息
        if data_list:
            # print(data_list, "data_list>>")
            info_dict = data_list[0]
            info_dict['roles'] = []

            for data in data_list:
                info_dict['roles'].append({
                    'roleid': data['rid'],
                    'role': data['role']
                })

            # 获取本机电脑名
            myname = socket.getfqdn(socket.gethostname())
            # 获取本机ip
            myaddr = socket.gethostbyname(myname)
            info_dict['sourceid'] = myaddr
            info_dict.pop('rid')
            info_dict.pop('role')
            # print(info_dict)

            return make_response(jsonify({
                'userInfo': info_dict,
            }))
        else:
            return make_response(jsonify({
                'userInfo': '',
            }))

    except AuthenticationError as error:
        current_app.logger.error('authentication error: %s', error)
        abort(403)
