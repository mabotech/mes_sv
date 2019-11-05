# -*- coding: utf-8 -*-
# @createTime    : 2019/10/28 10:20
# @author  : Huanglg
# @fileName: test13.py
# @email: luguang.huang@mabotech.com
import datetime
import random
for i in range (0,10):
  nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S") #生成当前时间
  randomNum=random.randint(0,100) #生成的随机整数n，其中0<=n<=100
  if randomNum<=10:
    randomNum=str(0)+str(randomNum)
  uniqueNum=str(nowTime)+str(randomNum)
  print(uniqueNum)
