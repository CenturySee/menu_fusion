#!/bin/python
#coding=utf8

import os
import re
import sys
import time
import json
import datetime
import traceback
import hashlib
try:
	import configparser as ConfigParser
except:
	import ConfigParser as ConfigParser
try:
	import pymysql as MySQLdb
except:
	import MySQLdb
import pymysql.cursors

cur_dir = os.path.dirname(os.path.abspath(__file__))
proj_dir = os.sep.join([cur_dir, '..'])
conf_dir = os.sep.join([proj_dir, 'conf'])
conf_fn = os.sep.join([conf_dir, 'db.conf'])
sec_name = 'mysql_test'

#logger = get_logger(__file__ + '.log')

# 获取自定义的mysql_obj
def get_mysql_obj(conf_fn, sec_name):
	cf_obj = ConfigParser.RawConfigParser()
	cf_obj.read(conf_fn)
	mysql_obj = {'ip': cf_obj.get(sec_name, 'ip'), \
							 'port': int(cf_obj.get(sec_name, 'port')), \
							 'password': cf_obj.get(sec_name, 'password'), \
							 'database': cf_obj.get(sec_name, 'database'), \
							 'user': cf_obj.get(sec_name, 'user')}
	mysql_obj['conn'] = MySQLdb.connect( \
			mysql_obj['ip'], mysql_obj['user'], mysql_obj['password'], \
			mysql_obj['database'], mysql_obj['port'], charset='utf8', \
			cursorclass=pymysql.cursors.DictCursor )
	mysql_obj['cursor'] = mysql_obj['conn'].cursor()
	return mysql_obj

if __name__ == '__main__':
	mysql_obj = get_mysql_obj(conf_fn, sec_name)
