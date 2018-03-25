#!/usr/bin/python
#coding=utf8

import os, re, sys, json
from collections import defaultdict

from directory_info import *

class MergeInfoStat():
    def __init__(self):
	pass 

    def get_stat_info(self, fn = '../data/merge_menu.res'):
	num = 0
	not_merged_set = set()
	fmt_str = '{:>5}'*7 + '\t{}'
	ls = ['b', 'e', 'm', 'be', 'bm', 'em', 'bem']
	for line in open(fn, 'r'):
	    ln = line.strip()
	    dic = json.loads(ln)
	    shop_info = dic['shop_info']
	    food_info = dic['food_info']
	    # 进行统计
	    num_dic = defaultdict(int) # b:baidu, e:eleme, m:meituan
	    unmerged_food_info = {}  # 未合并的菜品信息
	    for k, v_ls in food_info.items():
		if len(v_ls) == 1:
		    not_merged_set.add(k)
		    unmerged_food_info[k] = v_ls[0]
		    src = ''.join([v[0] for v in v_ls])
		    num_dic[src] += 1
		else:
		    src = ''.join([v[0] for v in sorted(v_ls)])
		    num_dic[src] += 1
	    # 打印单个店铺的统计信息
	    col0 = '_'.join([shop_info.get('baidu', '####'), \
		    shop_info.get('eleme', '####'), \
		    shop_info.get('meituan', '####')])
	    stat_info = [str(num_dic[k]) for k in ls] + [col0]
	    #print ('\t'.join(stat_info).encode('utf8'))
	    print (fmt_str.format(*stat_info))
	    unmerged_info = {'shop_info':shop_info, \
		    'unmerged_food_info':unmerged_food_info}
	    num += 1
	    #sys.stderr.write('{}\n'.format(json.dumps(unmerged_info, ensure_ascii=False).encode('utf8')))
	    #sys.stderr.write('\n'.join([ss.encode('utf8') for ss in unmerged_food_info.keys()]) + '\n') 
	    #sys.stderr.write('{}\n'.format('\n'.join([ss..encode('utf8') for ss in unmerged_food_info.keys()])))
	res_ls = sorted([ss.encode('utf8') for ss in not_merged_set])
	sys.stderr.write('\n'.join(res_ls) + '\n')

if __name__ == '__main__':
    merge_stat_obj = MergeInfoStat()
    merge_stat_obj.get_stat_info()
