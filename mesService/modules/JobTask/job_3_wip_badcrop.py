# -*- coding: utf-8 -*-
# @createTime    : 2019/12/27
# @author  : 王江桥
# @fileName: job_3_wip_badcrop.py
# @email: jiangqiao.wang@mabotech.com

import sys
# sys.path.append(r'C:\Users\mabot\Desktop\BFCEC\foton\mesService')
sys.path.append(r'/home/test01/mesService')


from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class WipBadcrop(object):

    def __init__(self):
        self.db = self.create_conn('development')

    def execteDatabase(self):
        """调用存储过程"""
        sql = "select job_wip_badcrop();"
        try:
            ret = self.db.query(sql)
            print(ret)
        except Exception as e:
            # current_app.logger.error(traceback.format_exc())
            print(e)

    def create_conn(self, config_name):
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db


if __name__ == '__main__':
    wd = WipBadcrop()
    wd.execteDatabase()
