# -*- coding: utf-8 -*-
# @createTime    : 2019/8/27 14:13
# @author  : Huanglg
# @fileName: __init__.py.py
# @email: luguang.huang@mabotech.com
from flask import Blueprint

auth_blue = Blueprint('auth',__name__)

from . import views
