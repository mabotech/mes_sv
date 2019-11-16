# -*- coding: utf-8 -*-
# @createTime    : 2019/11/16 12:53
# @author  : Huanglg
# @fileName: __init__.py.py
# @email: luguang.huang@mabotech.com
from flask import Blueprint

from mesService import constants

process_manage_blue = Blueprint('process_manage', __name__, url_prefix =constants.URL_PREFIX)

from . import views
