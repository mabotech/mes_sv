# -*- coding: utf-8 -*-
# @createTime    : 2019/8/27 14:13
# @author  : Huanglg
# @fileName: __init__.py.py
# @email: luguang.huang@mabotech.com
from flask import Blueprint

from mesService import constants

auth_blue = Blueprint('auth',__name__, url_prefix=constants.URL_PREFIX)

from . import views
