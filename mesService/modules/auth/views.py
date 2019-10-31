# -*- coding: utf-8 -*-
# @createTime    : 2019/8/27 14:13
# @author  : Huanglg
# @fileName: views.py
# @email: luguang.huang@mabotech.com
from flask import current_app, request, make_response, abort
from flask.json import jsonify

from .auth import (authenticate_user, AuthenticationError)
from . import auth_blue

@auth_blue.route('/test')
def test_auth():
    sql = "select name, employeeno, loginname, password, employeevaliddate, resourceid from employee"
    res = current_app.db.query(sql)
    return jsonify(res)



@auth_blue.route('/api/auth/login', methods=['POST'])
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
