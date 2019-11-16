# -*- coding: utf-8 -*-
# @createTime    : 2019/11/16 12:54
# @author  : Huanglg
# @fileName: views.py
# @email: luguang.huang@mabotech.com
import traceback
import os
import uuid

from flask import current_app, request, send_from_directory
from flask.json import jsonify
from werkzeug.utils import secure_filename

from mesService import constants
from . import process_manage_blue


@process_manage_blue.route('/upload', methods = ['POST'])
def upload():

    result = {
        "url": '',
        "uid": uuid.uuid4().hex,
        "name": '',
        "isSuccess": False
    }

    try:
        file = request.files.get('file')
        path = os.path.join(os.getcwd(), 'images')
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, file.filename))
        result['url'] = os.path.join('/get_image/', file.filename)
        result['name'] = file.filename
    except Exception:
        current_app.logger.error(traceback.format_exc())
        return jsonify(result)

    result['isSuccess'] = True
    return jsonify(result)

@process_manage_blue.route("/get_image/<filename>" , methods = ['GET'])
def get_image(filename):
    path = os.path.join(os.getcwd(), 'images')
    return send_from_directory(path, filename)
