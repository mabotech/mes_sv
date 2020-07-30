import sys
sys.path.append(r'/home/test01/messervice')


from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class Clear(object):

    def __init__(self):
        self.db = self.create_conn('development')

    def execteDatabase(self):
        """调用存储过程"""
        sql = "select update_ps();"     # 清除PS
        try:
            ret_badcrop = self.db.query(sql)
            print(ret_badcrop)
        except Exception as e:
            # current_app.logger.error(traceback.format_exc())
            print(e)

    def create_conn(self, config_name):
        """"""
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

if __name__ == '__main__':
    c = Clear()
    c.execteDatabase()
