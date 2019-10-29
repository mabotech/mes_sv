# -*- coding: utf-8 -*-
# @createTime    : 2019/10/28 13:27
# @author  : Huanglg
# @fileName: text_manage.py
# @email: luguang.huang@mabotech.com
import random
import time
import traceback

from flask import current_app

def tt_manage(medium, textid, languageid=2052):
    """

    :param medium: 描述
    :param textid: 0 是新增，其他是更新
    :param languageid: 默认2052
    :return:
    """
    if int(textid) == 0:
        # 生成textid
        textid = hash(time.time()) + random.randint(1, 1000)
        base_sql = "insert into TEXT_TRANSLATION(textid, languageid, medium) values ({textid}, {languageid}, '{medium}')"
        sql_str = base_sql.format(textid=textid, languageid=languageid, medium=medium)
        insert_result = None
        try:
            insert_result = current_app.db.execute(sql_str)
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return e
        if insert_result:
            return textid

    else:
        base_sql = "update TEXT_TRANSLATION set medium = '{medium}' where textid = {textid} and languageid={languageid}"
        sql_str = base_sql.format(medium=medium, textid=textid, languageid=languageid)
        result = None
        try:
            result = current_app.db.execute(sql_str)
        except Exception:
            current_app.logger.error(traceback.format_exc())
        if result:
            return textid

if __name__ == '__main__':
    tt_manage('BFCEC_虚拟件', 0)

