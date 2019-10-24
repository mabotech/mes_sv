# -*- coding: utf-8 -*-
# @createTime    : 2019/8/26 21:02
# @author  : Huanglg
# @fileName: __init__.py.py
# @email: luguang.huang@mabotech.com
import logging
from logging.handlers import RotatingFileHandler

from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager

from mesService.lib.pgwrap.db import connection
from flask import Flask
from .config import Config, config_dict


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config_dict[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler(
        "logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter(
        '%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    """
    The factory function，create application object
    :param config_name: 'development' or 'production'
    :return: application object
    """
    app = Flask(__name__)

    # logs
    setup_log(config_name)
    app.config.from_object(config_dict[config_name])

    # timed task
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    JWTManager(app)
    db = create_conn(config_name)
    app.db = db

    from .modules.auth import auth_blue
    app.register_blueprint(auth_blue)
    from .modules.systemConfig import system_config_blue
    app.register_blueprint(system_config_blue)

    return app



def create_conn(config_name):
    db_info = config_dict[config_name].DB_INFO
    db = connection(db_info)
    return db
