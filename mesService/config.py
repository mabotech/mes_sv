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
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    LOG_LEVEL = logging.DEBUG

    # 使用redis来保存session信息
    SESSION_TYPE = 'redis'
    # 对象session信息进行签名
    SESSION_USE_SIGNER = True
    # 存储session的redis实例
    SESSION_REDIS = StrictRedis(host = REDIS_HOST,port= REDIS_PORT )
    # 指定session的过期时间1天
    PERMANENT_SESSION_LIFETIME = 86400

    APPLICATION_TITLE = "Flask JWT Example"
    JWT_TOKEN_LOCATION = "headers"
    JWT_ACCESS_TOKEN_EXPIRES = 30
    JWT_REFRESH_TOKEN_EXPIRES = 600

    DB_INFO = {
        'database': 'flxuser',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'huanglg.top',
        'port': 5432,
    }

    # 定时任务
    JOBS = [
        # {  # 第一个任务
        #     'id': 'job1',
        #     'func': '__main__:job_1',
        #     'args': (1, 2),
        #     'trigger': 'cron', # cron表示定时任务
        #     'hour': 19,
        #     'minute': 27
        # },
        # 第二个任务，每隔5分钟执行一次
        # {
        #     'id': 'job2',
        #     'func': 'config:job_2',  # 方法名
        #     # 'args': (1, 2),  # 入参
        #     'trigger': 'interval',  # interval表示循环任务
        #     'seconds': 5,
        # }
    ]


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.ERROR

config_dict = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
}
