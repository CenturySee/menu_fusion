#!/usr/bin/python
# coding=utf8

import os
import sys
import json
import traceback
from collections import defaultdict, OrderedDict

cur_dir = os.path.dirname(os.path.abspath(__file__))
proj_dir = os.sep.join([cur_dir, '..'])
conf_dir = os.sep.join([proj_dir, 'conf'])
utils_dir = os.sep.join([proj_dir, 'utils'])

sys.path.append(utils_dir)
from mysql_operation import get_mysql_obj
from feature_generator import FeatureGenerator
from cluster import SimpleCluster

def menu_cluster(fn = 'merged_shop.json'):
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
    for line in open(fn, 'r'):
	dic = json.loads(line.strip())
	feat_ls = []
	for tag, _id in dic.items():
	    if tag not in tb_dic:
		continue
	    tb_name = tb_dic[tag]
	    cursor.execute(sql.format(tb_name, _id))
	    res = cursor.fetchone()
	    __feat_ls = feat_gen.generate_feature_with_food_dic(res, tag)
#	    print ('__feat_ls', len(__feat_ls))
	    feat_ls.extend(__feat_ls)
#	print (len(feat_ls), feat_ls)
	label_ls = cluster_obj.cluster(feat_ls)
	res_dic = OrderedDict()
	for __feat_ls, label in zip(feat_ls, label_ls):
	    if label not in res_dic:
		res_dic[label] = []
	    src, _id, food_dic, food_name = __feat_ls[:4]
	    food_dic['__source'] = src
	    food_dic['__id'] = _id
	    res_dic[label].append(food_dic)
	res_dic = {'id': dic['id'], 'foods':res_dic}
	print (json.dumps(res_dic, ensure_ascii=False).encode('utf8'))

if __name__ == '__main__':
    menu_cluster()
