# -*- coding: utf-8 -*-
# @createTime    : 2020/06/03
# @author  : 王江桥
# @fileName: mail_alarm.py
# @email: jiangqiao.wang@mabotech.com

import smtplib
from email.mime.text import MIMEText


def send_data(mail_list, title, content):
    """
    function: send mails
    :param mail_list: 邮箱列表信息，例:[{"mail":"11@qq.com"},..]
    :param title: "机加MES执行JOB错误-message"
    :param content: 邮件内容
    :return:
    """
    tolist = []  # 邮箱列表
    fromil = '248788461@qq.com'
    toil = mail_list[0]["mail"]

    for mail in mail_list:
        tolist.append(mail["mail"])

    send_mail(title, content, fromil, toil, tolist)


def send_mail(title, content, fromil, toil, tolist):
    """
    function: send mail
    :param title:
    :param content:
    :param fromil: 发送邮箱
    :param toil: 接收邮箱
    :param tolist: 接收邮箱列表
    :return:
    """
    # 本地测试
    # msg = MIMEText('自动维护成功，OPC数据采集正常', 'plain', 'utf-8')
    # msg['subject'] = '发送邮件测试'
    # msg['to'] = 'jiangqiao.wang@mabotech.com'
    # msg['from'] = '248788461@qq.com'
    # smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
    # sender = '248788461@qq.com'
    # password = 'pjtkhrnjuzmkbgii'
    # smtp.login(sender, password)
    # smtp.sendmail(sender, ['jiangqiao.wang@mabotech.com', 'cq_wangjiangqiao@163.com'], msg.as_string())
    # smtp.close()

    # print(title)
    # print(str(content))
    # print(fromil)
    # print(toil)
    # print(tolist)

    mail_content = """
    （1）错误内容：{0},\n
    （2）错误详情：{1}。
    """.format(title, content)

    msg = MIMEText(mail_content, 'plain', 'utf-8')
    msg['subject'] = str(title)
    msg['to'] = toil
    msg['from'] = fromil
    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
    sender = fromil
    password = 'pjtkhrnjuzmkbgii'
    smtp.login(sender, password)
    smtp.sendmail(sender, tolist, msg.as_string())  # tolist: 接收邮箱列表
    smtp.close()

    # 生产服务器
    # msg = MIMEText('自动维护成功，OPC数据采集正常', 'plain', 'utf-8')
    # msg['subject'] = '自动维护成功，OPC数据采集正常'
    # msg['to'] = 'jiangqiao.wang@mabotech.com'
    # msg['from'] = 'Crystalreport@cummins.com'
    # smtp = smtplib.SMTP_SSL('mailrelay.cummins.com', 25)
    # sender = 'Crystalreport@cummins.com'
    # password = ''
    # smtp.login(sender, password)
    # smtp.sendmail(sender, ['jiangqiao.wang@mabotech.com'], msg.as_string())
    # smtp.close()

    # cur.close()
    # conn.close()


if __name__ == "__main__":
    # send_mail()
    pass
