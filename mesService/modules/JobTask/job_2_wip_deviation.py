# -*- coding: utf-8 -*-
# @createTime    : 2019/12/24
# @author  : 王江桥
# @fileName: job_2_wip_deviation.py
# @email: jiangqiao.wang@mabotech.com


from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class WipDeviation(object):

    def __init__(self):
        self.db = self.create_conn('development')

    def execteDatabase(self):
        """调用存储过程"""
        sql = "select wip_deviation();"
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
    wd = WipDeviation()
    wd.execteDatabase()
