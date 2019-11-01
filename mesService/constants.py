# -*- coding: utf-8 -*-
# @createTime    : 2019/10/28 18:03
# @author  : Huanglg
# @fileName: constants.py
# @email: luguang.huang@mabotech.com

# 版本控制
URL_PREFIX = '/api/v1/'

# 定时循环时间 秒
LOOP_TIME = 30

# api返回值
RET = {
    'status': 200,
    'msg': 'success'
}

# 物料类型
PRODUCTINVENTORYTYPE_ENUM = {
    'BFCEC_半成品': 110,
    'BFCEC_采购件': 120,
    'BFCEC_虚拟件': 130,
    'BFCEC_通用类型': 100
}

# BOM物料类型
BOM_ENUM = {
    'BFCEC_采购件': 1,
    'BFCEC_虚拟件': 2,
}

# 物料状态
STATUS_ENUM = {
    "Active": 1,
    "inActive": 0
}

# 偏离类型(A:增加或者D:删除)
ACTIONS_ENUM = {
    "A": 1,
    "D": 0
}


