# -*- coding: utf-8 -*-
# @createTime    : 2020/03/25 22:03
# @author  : 王江桥
# @fileName: app_main.py
# @email: jiangqiao.wang@mabotech.com


import app
from multiprocessing import Process
from mesService.modules.RabbitMQ import interface_con


def app_app():
    print(app.app.url_map)
    app.app.run(host='0.0.0.0')


def app_interface():
    interface_con.main()


if __name__ == '__main__':
    # print(app.app.url_map)
    # app.app.run(debug=True, host='0.0.0.0')
    Process(target=app_app).start()
    Process(target=app_interface).start()
