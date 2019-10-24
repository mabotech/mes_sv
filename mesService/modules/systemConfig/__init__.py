# -*- coding: utf-8 -*-
# @createTime    : 2019/8/30 10:05
# @author  : Huanglg
# @fileName: __init__.py.py
# @email: luguang.huang@mabotech.com
from flask import Blueprint

system_config_blue = Blueprint('system_config',__name__)

from . import views
