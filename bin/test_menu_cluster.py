#!/usr/bin/python
# coding=utf8

import os
import sys
import json
import traceback
from collections import defaultdict

cur_dir = os.path.dirname(os.path.abspath(__file__))
proj_dir = os.sep.join([cur_dir, '..'])
conf_dir = os.sep.join([proj_dir, 'conf'])
utils_dir = os.sep.join([proj_dir, 'utils'])

sys.path.append(utils_dir)
from mysql_operation import get_mysql_obj
from feature_generator import FeatureGenerator
from cluster import SimpleCluster

def menu_cluster(fn = '../menu_fusion/res_dic.json'):
    '''
    进行菜品的聚类
    input: fn string 合并好的文件名 一行一个合并的店铺 {"baidu":'', "eleme":'', "meituan":'', "id":''}
    output: 打印结果 json 每行为一个店铺的菜品合并信息
    '''
    sql = "select * from `{}` where id='{}'"
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_online')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']

    feat_gen = FeatureGenerator()
    cluster_obj = SimpleCluster()
 
    tb_dic = {'eleme':'eleme_shop', 'baidu':'baidu_waimai_shop', 'meituan':'meituan_waimai_shop'}
    num = 0
    for line in open(, 'r'):
	dic = json.loads(line.strip())
	feat_ls = []
	for tag, _id in dic.items():
	    tb_name = tb_dic[tag]
	    cursor.execute(sql.format(tb_name, _id))
	    res = cursor.fetchone()
	    __feat_ls = feat_gen.generate_feature_with_food_dic(res, tb_name)
#	    print ('__feat_ls', len(__feat_ls))
	    feat_ls.extend(__feat_ls)
#	print (len(feat_ls), feat_ls)
	label_ls = cluster_obj.cluster(feat_ls)
	out_ls = []
	for __feat_ls, label in zip(feat_ls, label_ls):
	    __feat_ls.append(str(label))
	    _feat_ls = []
	    for ss in __feat_ls:
		if not isinstance(ss, str):
		    ss = ss.encode('utf8')
		_feat_ls.append(ss)
	    out_ls.append(_feat_ls)
	out_ls = sorted(out_ls, key=lambda x:x[-1])
	for _feat_ls in out_ls:
	    print ('\t'.join(_feat_ls))
	print ''
	num += 1
	if num == 10:
	    break
#	if len(label_ls) == label_ls[-1] + 1:
#	    continue
#	print (label_ls)
#	res_dic = defaultdict(list)
#	for label, feat_tup in zip(label_ls, feat_ls):    
#	    res_dic[label].append(feat_tup)
#	value_ls = sorted(res_dic.values(), key=lambda x:-len(x))
#	for val_ls in value_ls:
#	    print (json.dumps(val_ls, ensure_ascii=False).encode('utf8'))
#	sys.exit()

if __name__ == '__main__':
    test_menu_cluster()
