# -*- coding: utf-8 -*-
# @createTime    : 2019/12/4 15:15
# @author  : Huanglg
# @fileName: RedisHelper.py
# @email: luguang.huang@mabotech.com
from mesService import redis_store


class RedisHelper:

    def __init__(self, sub_channel = None, pub_channel = None):
        self.__conn = redis_store
        self.sub_channel = sub_channel
        self.pub_channel = pub_channel

    def pub(self, msg):
        self.__conn.publish(self.pub_channel, msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.sub_channel)
        pub.parse_response()
        return pub
