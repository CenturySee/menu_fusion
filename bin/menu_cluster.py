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
from cluster import SimpleCluster
from metrics import Metrics
from str_normalizer import StringNormalizer

def menu_cluster():
    norm_obj = StringNormalizer()
    cluster_obj = SimpleCluster()
    metrics_obj = Metrics()

    feat_tup_ls, classes = [], []
    head_ls = ['_id', 'food_length', 'purity', 'inv_purity', 'brand_name']
    head_fmt_str = '{:>35} {:>11}   {:<8} {:<15}  {}'
    print (head_fmt_str.format(*head_ls))
    content_fmt_str = '{:>35} {:>11}   {:<8.3f} {:<15.3f} {}'
    for line in open('../data/labeled_data_0328.tsv', 'r'):
	ln = line.strip()
	tup_ls = ln.split('    ')
	if not ln:
	    if not feat_tup_ls:
		continue
	    # 进行纯度计算
	    label_ls = cluster_obj.cluster(feat_tup_ls)
	    if len(label_ls) != len(classes):
		sys.stderr.write('_id: {} not labeled correctly\n'.format(_id))
	    else:
		#wrong_dic = metrics_obj.impure_case(label_ls, classes, feat_tup_ls)
		wrong_dic = metrics_obj.impure_case(classes, label_ls, feat_tup_ls)
		wrong_dic['_id'] = _id
		sys.stderr.write('{}\n'.format(json.dumps(wrong_dic, ensure_ascii=False)))
		#sys.stderr.write('{}\n'.format(json.dumps(wrong_dic, ensure_ascii=False)))
		purity = metrics_obj.purity(label_ls, classes)
		inv_purity = metrics_obj.purity(classes, label_ls)
		res_ls = [_id.encode('utf8'), len(label_ls), purity, inv_purity, brand_name]
		print content_fmt_str.format(*res_ls)
		#print ('_id: {}, brand_name: {}, food_length: {}, purity: {}, class_len/label_len: {}'.format(_id, brand_name, len(label_ls), purity, 1.0*class_len/label_len))
	    feat_tup_ls, classes = [], []
	    continue
	try:
	    _id, brand_name, food, src_id, src, label = tup_ls
	    norm_food = norm_obj.normalize(food)
	    feat_tup = [src, src_id, brand_name, food, norm_food]
	    feat_tup_ls.append(feat_tup)
	    classes.append(int(label))
	except:
	    print ln
	    traceback.print_exc()
	    sys.exit()
	    continue
    if feat_tup_ls:
        label_ls = cluster_obj.cluster(feat_tup_ls)
        if len(label_ls) != len(classes):
	    sys.stderr.write('_id: {} not labeled correctly\n'.format(_id))
	else:
	    purity = metrics_obj.purity(label_ls, classes)
	    inv_purity = metrics_obj.purity(classes, label_ls)
	    res_ls = [_id.encode('utf8'), len(label_ls), purity, inv_purity, brand_name]
	    print content_fmt_str.format(*res_ls)


if __name__ == '__main__':
    menu_cluster()
