import sys,os,time
sys.path.append(r'/home/test01/messervice')


from mesService import config_dict
from mesService.lib.pgwrap.db import connection


class Ces(object):

    def __init__(self):
        self.db = self.create_conn('production')

    def execteDatabase(self,path):
        """调用存储过程"""

        list_name = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            datas = os.path.splitext(file_path)[0].split(';')[1]
            # print(datas)
            time.sleep(3)
            sql = """SELECT mesn FROM serial_no_record WHERE serialno ILIKE '%{}%'"""
            try:
                ret_badcrop = self.db.query(sql.format(datas))
                print(ret_badcrop[0]['mesn'])
            except Exception as e:
                # current_app.logger.error(traceback.format_exc())
                print(e)

    def create_conn(self, config_name):
        """"""
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

if __name__ == '__main__':
    c = Ces()
    c.execteDatabase('C:\\Users\\sunho\\Desktop\\27\\27')
