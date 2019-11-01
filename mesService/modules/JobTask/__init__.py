# -*- coding: utf-8 -*-
# @createTime    : 2019/11/1 9:43
# @author  : Huanglg
# @fileName: __init__.py.py
# @email: luguang.huang@mabotech.com

# 定时任务入口
import requests

from mesService.modules.ERPInterface.mes_to_erp.iac.send_iac import IacToXml


def start_job_task():

    test_iac()


def test_iac():

    "IAC 测试"

    iac = IacToXml()
    data = iac.get_iac_data()
    xml_str = iac.dict_to_xml(data[0]).decode('utf-8')
    send_to_test_interface(xml_str)

def send_to_test_interface(payload):

    url = "http://127.0.0.1:5000/api/v1/receive_data"

    headers = {
        'content-type': "application/xml",
        'cache-control': "no-cache",
        'postman-token': "436bc3d2-f88a-20a7-7280-3181289b8e71"
    }

    try:
        requests.request("POST", url, data=payload, headers=headers)
    except Exception as e:
        print(e)
