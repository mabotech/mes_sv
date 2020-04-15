# -*- coding: utf-8 -*-
# @createTime    : 2019/11/16 12:54
# @author  : Huanglg
# @fileName: views.py
# @email: luguang.huang@mabotech.com
import json
import traceback
import os
import uuid

from flask import current_app, request, send_from_directory
from flask.json import jsonify

from mesService import constants
from . import avatar_manage_blue


@avatar_manage_blue.route('/avatar', methods=['POST'])
def avatar():
    result = {
        "url": '',
        "uid": uuid.uuid4().hex,
        "name": '',
        "isSuccess": True
    }

    try:
        BASE_DIR = os.path.join(os.getcwd(), 'images')
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

        file = request.files.get('file')
        username = request.form.get('username')
        # filename = file.filename
        filename = username + "_avatar.jpg"
        print("username>>", username)
        print("filename>>", filename)

        image_url = os.path.join('/get_avatar/', filename)
        file.save(os.path.join(BASE_DIR, filename))

        # 图片信息存入数据库
        params = {
            "loginname": username,
            "pictureurl": image_url
        }

        sql_str = "select insert_employee_pictureurl('{}')".format(json.dumps(params))
        db_result = current_app.db.query_one(sql_str)[0]

        if db_result != 1:
            result['isSuccess'] = False

        result['url'] = image_url
        result['name'] = filename
    except Exception:
        current_app.logger.error(traceback.format_exc())
        result['isSuccess'] = False
        return jsonify(result)

    return jsonify(result)


@avatar_manage_blue.route("/get_avatar/<filename>", methods=['GET'])
def get_image(filename):
    path = os.path.join(os.getcwd(), 'images')
    return send_from_directory(path, filename + "_avatar.jpg")
