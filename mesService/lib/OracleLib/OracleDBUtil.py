# -*- coding: utf-8 -*-
# @createTime    : 2019/4/12 9:11
# @author  : Huanglg
# @fileName: OracleDBUtil.py
# @email: luguang.huang@mabotech.com
import traceback

import cx_Oracle
import re
import time
from .config import config
from logging import getLogger


log = getLogger('datasv')


class Oracle(object):
    def __init__(self, conf=None):
        if not conf:
            self.conf = config
        self.host = self.conf.get('host', '127.0.0.1')
        self.port = self.conf.get('port', 1521)
        self.user = self.conf.get('user', '')
        self.passwd = self.conf.get('passwd', '')
        self.db = self.conf.get('db')
        self.dsn = cx_Oracle.makedsn(
            self.host,
            self.port,
            self.db,
        )

    def ping_server(self):
        try:
            self.conn = cx_Oracle.connect(
                self.user,
                self.passwd,
                self.dsn,
                encoding="UTF-8", nencoding="UTF-8"
            )
        except Exception as e:
            log.error(traceback.format_exc())
            time.sleep(2)
            return self.ping_server()

    def query(self, sql):
        try:
            self.ping_server()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            desc = cursor.description
            self.result_to_dict(result, desc)
            return self.result_to_dict(result, desc)
        except Exception as e:
            log.error(e)
        finally:
            try:
                cursor.close()
                self.conn.close()
            except Exception:
                log.error(traceback.format_exc())

    def result_to_dict(self, res, desc):
        columnNames = [d[0].lower() for d in desc]
        result = []
        for item in res:
            item = dict(zip(columnNames, item))
            result.append(item)
        return result

    def execut(self, sql, params=''):
        try:
            self.ping_server()
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            log.error(e)
        finally:
            try:
                cursor.close()
                self.conn.close()
            except Exception:
                log.error(traceback.format_exc())


    def call_proc(self, proc, in_param, var_num=0, num=0):
        try:
            self.ping_server()
            cursor = self.conn.cursor()
            rtnId = [cursor.var(cx_Oracle.NUMBER)
                     for v in range(num)]
            rtnMsg = [cursor.var(cx_Oracle.STRING)
                      for v in range(var_num)]

            param = tuple(rtnId) + in_param + tuple(rtnMsg)

            # print(param)

            cursor.callproc(proc, param)

            return [v.getvalue() for v in rtnMsg]
        except cx_Oracle.Error as exc:
            # error, =  exc.args
            log.error(exc)
            return None
        finally:
            try:
                cursor.close()
                self.conn.close()
            except Exception:
                pass
