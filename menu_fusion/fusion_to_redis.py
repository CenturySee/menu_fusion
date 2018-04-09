#!/bin/python
#coding=utf8

import sys
import json
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
r = redis.Redis(connection_pool=pool)
for line in open('food_fusion.json', 'r'):
    ln = line.strip()
    dic = json.loads(ln)
    _id = dic['id']
    r.set(_id, ln)
