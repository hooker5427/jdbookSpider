# -*- coding: utf-8 -*-
# @Time    : 2020-07-06 16:07
# @Author  : hooker5427

import redis

myredis = redis.Redis(host='47.115.21.129', port=6379, password='redis')

with open('link.txt', 'r', encoding='utf-8')  as file:
    for line in file.readlines():
        mylist = line.split('#######')
        url = mylist[-1].strip('\n')
        myredis.lpush("jd:start_urls", url)
