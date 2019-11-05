# @createTime    : 2019/10/30 10:13
# @author  : Mou
# @fileName: send_data.py
import re
import time
import json
from mesService import constants
from flask import views
from flask import Blueprint
from flask import current_app
from flask.json import jsonify
from .planmanage import plan_schedule

bom = Blueprint("bom", __name__, url_prefix=constants.URL_PREFIX)
wipsortlist = Blueprint("wipsortlist",  __name__, url_prefix=constants.URL_PREFIX)


class WipSortlist(views.MethodView):
    """
    工单排序接口，获取工单排序的展示数据
    数据库：postgres
    """
    method = ["GET", "POST"]
    def get(self):
        result = {
            "status":"error",
            "message":"illegal request"
        }
        res = jsonify(result)
        return res
    def post(self):
        planschedule = plan_schedule.PlanSchedule()
        res = planschedule.getsortlist()
        return jsonify(res)
wipsortlist.add_url_rule("/wipsortlist", view_func=WipSortlist.as_view(name="wipsortlist"))