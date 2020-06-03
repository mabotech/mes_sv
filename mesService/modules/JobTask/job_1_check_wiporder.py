# -*- coding: utf-8 -*-
# @createTime    : 2019/12/24
# @author  : 王江桥
# @fileName: job_1_check_wiporder.py
# @email: jiangqiao.wang@mabotech.com

import sys

# sys.path.append(r'C:\Users\mabot\Desktop\BFCEC\foton\mesService')
sys.path.append(r'/home/test01/mesService')

import os
import json
import hashlib
from mesService import config_dict
from mesService.lib.pgwrap.db import connection
from mesService.lib.redisLib.RedisHelper import RedisHelper
from mesService.modules.JobTask import mail_alarm

# 全局字典
CHECK_DICT = {}


class CheckWipOrder(object):

    def __init__(self):
        self.db = self.create_conn('development')
        self.red = RedisHelper()

    def execteDatabase(self):
        """调用存储过程"""

        # 获取接收邮箱列表
        mail_list = self.query()
        # 文件名称
        # basename = os.path.basename(__file__)

        sql = "select job_check_wiporder();"
        try:
            ret = self.db.query(sql)
            result = ret[0]["job_check_wiporder"]
            # print(result)

            check_data_info = result.get("check_data_info", None)  # 所有待校验的工单信息日志
            processid_err_log = result.get("processid_err_log", None)  # processid不存在日志
            result_data = result.get("result_data", None)  # 执行结果
            bom_data_nonexistent_err_log = result.get("bom_data_nonexistent_err_log", None)  # bom数据不存在日志
            bom_data_inconformity_err_log = result.get("bom_data_inconformity_err_log", None)  # 工位bom和基础bom数据不一致日志

            print(result_data)
            # print(check_data_info)
            # print(processid_err_log)
            # print(bom_data_nonexistent_err_log)
            # print(bom_data_inconformity_err_log)

            # md5数据查重
            # 所有待校验的工单信息日志
            check_data_info_value = self.red.get_hash("job_1_check_wiporder", "check_data_info")
            check_data_info_md5_value = self.data_md5(str(check_data_info))
            if check_data_info_value == check_data_info_md5_value:
                pass
            else:
                # 存储redis
                self.red.set_hash("job_1_check_wiporder", "check_data_info", check_data_info_md5_value)
                # 写入日志
                self.insert_log(check_data_info)

            # processid不存在日志
            processid_err_log_value = self.red.get_hash("job_1_check_wiporder", "processid_err_log")
            processid_err_log_md5_value = self.data_md5(str(processid_err_log))
            if processid_err_log_value == processid_err_log_md5_value:
                pass
            else:
                self.red.set_hash("job_1_check_wiporder", "processid_err_log", processid_err_log_md5_value)
                self.insert_log(processid_err_log)
                # 邮件标题
                basename = "机加MES执行JOB错误-" + processid_err_log.get("message", None)
                # 发送邮件
                mail_alarm.send_data(mail_list, basename, processid_err_log)

            # bom数据不存在日志
            bom_data_nonexistent_err_log_value = self.red.get_hash("job_1_check_wiporder",
                                                                   "bom_data_nonexistent_err_log")
            bom_data_nonexistent_err_log_md5_value = self.data_md5(str(bom_data_nonexistent_err_log))
            if bom_data_nonexistent_err_log_value == bom_data_nonexistent_err_log_md5_value:
                pass
            else:
                self.red.set_hash("job_1_check_wiporder", "bom_data_nonexistent_err_log",
                                  bom_data_nonexistent_err_log_md5_value)
                self.insert_log(bom_data_nonexistent_err_log)
                # 邮件标题
                basename = "机加MES执行JOB错误-" + bom_data_nonexistent_err_log.get("message", None)
                # 发送邮件
                mail_alarm.send_data(mail_list, basename, bom_data_nonexistent_err_log)

            # 工位bom和基础bom数据不一致日志
            bom_data_inconformity_err_log_value = self.red.get_hash("job_1_check_wiporder",
                                                                    "bom_data_inconformity_err_log")
            bom_data_inconformity_err_log_md5_value = self.data_md5(str(bom_data_inconformity_err_log))
            if bom_data_inconformity_err_log_value == bom_data_inconformity_err_log_md5_value:
                pass
            else:
                self.red.set_hash("job_1_check_wiporder", "bom_data_inconformity_err_log",
                                  bom_data_inconformity_err_log_md5_value)
                self.insert_log(bom_data_inconformity_err_log)
                # 邮件标题
                basename = "机加MES执行JOB错误-" + bom_data_inconformity_err_log.get("message", None)
                # 发送邮件
                mail_alarm.send_data(mail_list, basename, bom_data_inconformity_err_log)

        except Exception as e:
            # current_app.logger.error(traceback.format_exc())
            print(e)

    def create_conn(self, config_name):
        db_info = config_dict[config_name].DB_INFO
        db = connection(db_info)
        return db

    def data_md5(self, data):
        """
        function:md5加密
        :param data:
        :return:
        """
        m = hashlib.md5()
        b = data.encode(encoding='utf-8')
        m.update(b)
        return m.hexdigest()

    def insert_log(self, data):
        """调用存储过程"""
        sql = """select job_insert_log('{0}');""".format(json.dumps(data))
        try:
            ret = self.db.query(sql)
            print("ret>>", ret)
            pass

        except Exception as e:
            print(e)

    def query(self):
        """mail query"""
        sql = """select mail from mail_log where active=1"""
        try:
            mail_list = self.db.query(sql)
            # print("ret>>", ret)
            return mail_list

        except Exception as e:
            print(e)


if __name__ == '__main__':
    cw = CheckWipOrder()
    cw.execteDatabase()
