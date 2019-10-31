# @createTime    : 2019/10/30 9:13
# @author  : Mou
# @fileName: plan-schedule.py
# 计划排产部分前端接口
import json
from flask import current_app
from flask import request
from mesService import config_dict
from mesService.lib.pgwrap.db import connection

class PlanSchedule(object):  
    def getsortlist(self):
        reqparam = request.data
<<<<<<< HEAD
=======
        result = False
>>>>>>> fcdb3b309fd730deb9a54fb736fe9bd60e995b0c
        try:
            reqparam = json.loads(reqparam)
            count = reqparam['count']
            wipordertype = reqparam['wipordertype']
            base_sql = "select get_wipsortlist(%d,%d);"%(count,wipordertype)
            result = current_app.db.query_one(base_sql)
        except:
            pass
        if result:
            return result[0]
        else:
            result = {
                "status":"error",
                "message":"search error"
            }
            res = json.dumps(result)
            return res 
        