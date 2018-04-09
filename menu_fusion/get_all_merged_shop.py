#!/bin/python
#coding=utf8

import os
import sys
import json
import random
from collections import defaultdict

wm_log_fn = '/home/chaoli/graph_waimai/src/normalize_pingce/waimai.log'
merged_shop_fn = '/data/task/graph_waimai/src/normalize/res.out_json_online'

def load_merged_info():
    merged_dic = defaultdict(dict)
    for line in open(merged_shop_fn, 'r'):
	ln = line.strip().decode('utf8')
	dic = json.loads(ln)
	for v in dic.values():
	    merged_dic[v] = dic
    #print ('merged_dic length', len(merged_dic))
    return merged_dic

def load_log_info():
    log_ls = []
    for line in open(wm_log_fn, 'r'):
	ln = line.strip().decode('utf8')
	ls = ln.split('\t')
	log_ls.append(ls)
    #print ('log length', len(log_id_ls))
    return log_ls

def random_sample(num = 1000000):
    log_ls = load_log_info()
    merged_dic = load_merged_info()
    random.shuffle(log_ls)
    cnt = 0
    for ls in log_ls:
	_id = ls[0]
	if _id in merged_dic:
	    dic = merged_dic[_id]
	    dic['id'] = _id
	    print (json.dumps(dic, ensure_ascii=False))
#	    ls.append(dic.get('meituan', ''))
#	    ls.append(dic.get('eleme', ''))
#	    ls.append(dic.get('baidu', ''))
#	    print ('\t'.join(ls).encode('utf8'))
#	    cnt += 1
#	if cnt >=num:
#	    break

if __name__ == '__main__':
    random_sample()

