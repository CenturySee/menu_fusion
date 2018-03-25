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

def test_menu_cluster():
    sql = "select * from `{}` where id='{}'"
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_waimai')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']

    feat_gen = FeatureGenerator()
    cluster_obj = SimpleCluster()
 
    tb_dic = {'eleme':'eleme_shop', 'baidu':'baidu_waimai_shop', 'meituan':'meituan_waimai_shop'}
    for line in open('../data/res.out_json_offline', 'r'):
	dic = json.loads(line.strip())
	feat_ls = []
	for tag, _id in dic.items():
	    tb_name = tb_dic[tag]
	    cursor.execute(sql.format(tb_name, _id))
	    res = cursor.fetchone()
	    __feat_ls = feat_gen.generate_feature(res, tb_name)
#	    print ('__feat_ls', len(__feat_ls))
	    feat_ls.extend(__feat_ls)
#	print (len(feat_ls), feat_ls)
	label_ls = cluster_obj.cluster(feat_ls)
	if len(label_ls) == label_ls[-1] + 1:
	    continue
#	print (label_ls)
	res_dic = defaultdict(list)
	for label, feat_tup in zip(label_ls, feat_ls):    
	    res_dic[label].append(feat_tup)
	value_ls = sorted(res_dic.values(), key=lambda x:-len(x))
	for val_ls in value_ls:
	    print (json.dumps(val_ls, ensure_ascii=False).encode('utf8'))
	sys.exit()

if __name__ == '__main__':
    test_menu_cluster()
