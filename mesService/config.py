# -*- coding: utf-8 -*-
# @createTime    : 2019/8/26 21:07
# @author  : Huanglg
# @fileName: config.py
# @email: luguang.huang@mabotech.com
# 将session信息储存到redis中，创建redis数据库的链接
import logging

from redis import StrictRedis


class Config(object):
    DEBUG = None

    SECRET_KEY = 'heyKyqaUgg8jAJJvjwxy3bUCkBFBX5ao3kK0HLptbW8='

    # 配置redis的主机和端口
    REDIS_HOST = '192.168.97.188'
    REDIS_PORT = 6379

    LOG_LEVEL = logging.WARNING

    # 使用redis来保存session信息
    SESSION_TYPE = 'redis'
    # 对象session信息进行签名
    SESSION_USE_SIGNER = True
    # 存储session的redis实例
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 指定session的过期时间1天
    PERMANENT_SESSION_LIFETIME = 86400
    RABBITMQ_HOST = '127.0.0.1'
    RABBITMQ_USER = 'guest'
    RABBITMQ_PASSWORD = 'guest'
    RABBITMQ_VHOST = '/'


    APPLICATION_TITLE = "Flask JWT Example"
    JWT_TOKEN_LOCATION = "headers"
    JWT_ACCESS_TOKEN_EXPIRES = 6000
    JWT_REFRESH_TOKEN_EXPIRES = 6000

    DB_INFO = {
        'database': 'BFCEC',
        'user': 'postgres',
        'password': 'postgres',
        'host': '192.168.97.188',
        'port': 5432,
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    DB_INFO = {
        'database': 'BFCEC',
        'user': 'postgres',
        'password': 'Mabotech123',
        'host': '192.168.220.57',
        'port': 5432,
    }
    REDIS_HOST = '192.168.220.57'
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    JWT_REFRESH_TOKEN_EXPIRES = 86400
    LOG_LEVEL = logging.ERROR
    RABBITMQ_HOST = '192.168.220.57'
    RABBITMQ_USER = 'admin'
    RABBITMQ_PASSWORD = 'python03$'
    RABBITMQ_VHOST = 'machining'



config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

CURRENT_ENV = 'development'

INTERFACE_BASE_URL = "http://127.0.0.1:5000"
INTERFACE_CLASS_NAME = {
    f"{INTERFACE_BASE_URL}/api/v1/deviation": "DeviationOrder",
    f"{INTERFACE_BASE_URL}/api/v1/item": "ItemOrder",
    f"{INTERFACE_BASE_URL}/api/v1/bom": "BomOrder",
    f"{INTERFACE_BASE_URL}/api/v1/wiporder": "WipOrderInterface",
    f"{INTERFACE_BASE_URL}/api/v1/wipsequence": "SequenceInterface"
}

# 工作模式
PRESENT_WORK_MODE = {
    "develp": "development",
    "test": "development",
    "production": "production"
}

# 当前工作模式
PRESENT_WORK_MODE = PRESENT_WORK_MODE["develp"]
