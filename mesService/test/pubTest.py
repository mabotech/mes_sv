# -*- coding: utf-8 -*-
# @createTime    : 2019/12/4 16:43
# @author  : Huanglg
# @fileName: pubTest.py
# @email: luguang.huang@mabotech.com
# 发布
import sys
sys.path.append('/home/huanglg/mesService')

from mesService.lib.redisLib.RedisHelper import RedisHelper


def pubTest():
    obj = RedisHelper('fm104.5', 'fm104.5')
    while True:
        msg = input('>>:')
        obj.pub(msg)

if __name__ == '__main__':
    pubTest()
