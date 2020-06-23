# -*- coding: utf-8 -*-
# @createTime    : 2019/12/4 15:15
# @author  : Huanglg
# @fileName: RedisHelper.py
# @email: luguang.huang@mabotech.com
from mesService import redis_store


class RedisHelper:

    def __init__(self, sub_channel=None, pub_channel=None):
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

    def set_hash(self, name, k, v):
        """
        function:set hash value
        :param name:job name
        :param k:
        :param v:
        :return:
        """
        self.__conn.hset(name, k, v)

    def get_hash(self, name, k):
        """
        function:get hash value
        :param name:job name
        :param k:
        :return:
        """
        return self.__conn.hget(name, k)
