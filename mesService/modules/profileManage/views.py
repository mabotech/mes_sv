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
from werkzeug.utils import secure_filename

from mesService import constants
from . import avatar_manage_blue


@avatar_manage_blue.route('/avatar', methods=['POST'])
def avatar():
    print(12345)
    # result = {
    #     "url": '',
    #     "uid": uuid.uuid4().hex,
    #     "name": '',
    #     "isSuccess": True
    # }
    #
    # try:
    #     BASE_DIR = os.path.join(os.getcwd(), 'images')
    #     if not os.path.exists(BASE_DIR):
    #         os.makedirs(BASE_DIR)
    #
    #     file = request.files.get('file')
    #     username = request.form.get('username')
    #     filename = file.filename
    #     file_format = filename.split('.')[-1]
    #     print("username", username)
    #     print("file_format", file_format)

    #     # 防止文件名重复，生成新的文件名
    #     new_filename = uuid.uuid1().hex + '_' + filename
    #     image_url = os.path.join('/get_image/', new_filename)
    #
    #     file.save(os.path.join(BASE_DIR, new_filename))
    #
    #     # 图片信息存入数据库
    #     params = {
    #         "name": filename.split('.')[0],  # 去掉扩展名
    #         "documenttypecode": documenttype,  # 扩展名
    #         "schemaurlflag": image_url,
    #         "username": username,
    #         "documentformat": file_format
    #     }
    #
    #     sql_str = "select insert_document('{}')".format(json.dumps(params))
    #     db_result = current_app.db.query_one(sql_str)[0]
    #
    #     if db_result != 1:
    #         result['isSuccess'] = False
    #
    #     result['url'] = image_url


    #     result['url'] = 111
    #     result['name'] = filename
    # except Exception:
    #     print(111)
    #     current_app.logger.error(traceback.format_exc())
    #     result['isSuccess'] = False
    #     return jsonify(result)
    #
    # return jsonify(result)


# @avatar_manage_blue.route("/get_image/<filename>", methods=['GET'])
# def get_image(filename):
#     path = os.path.join(os.getcwd(), 'images')
#     return send_from_directory(path, filename)
