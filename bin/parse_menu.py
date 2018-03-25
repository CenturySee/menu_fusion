#!/usr/bin/python
# coding=utf8

import os
import sys
import json
import zlib
import base64
import traceback

cur_dir = os.path.dirname(os.path.abspath(__file__))
proj_dir = os.sep.join([cur_dir, '..'])
conf_dir = os.sep.join([proj_dir, 'conf'])
utils_dir = os.sep.join([proj_dir, 'utils'])

sys.path.append(utils_dir)
from mysql_operation import get_mysql_obj

#from WebSpider.util import jsonCompress, jsonDecompress
from meituan_waimai_parser import MtWmParser
from baidu_waimai_parser import BdWmParser
from eleme_parser import ElemeParser
from menu_merger import MenuMerger

def jsonDecompress(content):
    try:
        return json.loads(zlib.decompress(base64.decodestring(content)))
    except:
	traceback.print_exc()
        return content

def parse_meituan_menu(ori_ss):
    '''
    parse meituan menu
    '''
#    ori_ss = jsonDecompress(ss)
#    if ori_ss == ss:
#	return
#    print (type(ori_ss))
#    return
    for base_dic in ori_ss:
	print json.dumps(base_dic, ensure_ascii=False).encode('utf8')
#	name = base_dic.get('name', '--')
#	print ('\t'.join(['name', name])).encode('utf8')
#	spus_ls = base_dic.get('spus', [])
#	for sp_dic in spus_ls:
#	    name = sp_dic.get('name', '')
#	    if name:
#		print(name.encode('utf8'))
##	    print ('\t'.join(['\t', 'name', sp_dic.get('name', '--'), str(sp_dic.get('min_price', '--'))])).encode('utf8')

def parse_eleme_menu(ori_ss):
#    ori_ss = jsonDecompress(ss)
#    print ('ori_ss type', type(ori_ss))
    ori_ss = json.loads(ori_ss)
#    print ('ori_ss type', type(ori_ss))
    ori_ss = json.loads(ori_ss)
#    print ('ori_ss type', type(ori_ss))
    # 进行内容的解析  list
#    print (len(ori_ss))
    #print json.dumps(ori_ss[0], ensure_ascii=False).encode('utf8')
    for base_dic in ori_ss:
#	print (json.dumps(base_dic, ensure_ascii=False)).encode('utf8')
#	name = base_dic.get('name', '--')
##	print ('\t'.join(['name', name])).encode('utf8')
	foods = base_dic.get('foods', [])
	for food_dic in foods:
	    print (food_dic.get('name', '').encode('utf8'))
#	    specfoods = food_dic.get('specfoods', [])
#	    for sp_dic in specfoods:
#	        name = sp_dic.get('name', '')
#	        if name:
#		    print(name.encode('utf8'))
#	    print ('\t'.join(['\t', 'name', sp_dic.get('name', '--'), str(sp_dic.get('price', '--'))])).encode('utf8')

def parse_baidu_menu(ori_ss):
#    ori_ss = jsonDecompress(ss)
#    print ('ori_ss type', type(ori_ss))
    ori_ss = json.loads(ori_ss)
#    print ('ori_ss type', type(ori_ss))
    # 进行内容的解析  dict
    # print (json.dumps(ori_ss, ensure_ascii=False).encode('utf8'))
    if isinstance(ori_ss, dict):
	ori_ss = list(ori_ss.values())
#	sys.stderr.write('{}\n'.format(json.dumps(ori_ss[0], ensure_ascii=False).encode('utf8')))
#	return
    for v_dic in ori_ss:
	print (json.dumps(v_dic, ensure_ascii=False)).encode('utf8')
#	catalog = v_dic.get('catalog', '--')
##	print ('\t'.join(['catalog', catalog])).encode('utf8')
#	data_dic_ls = v_dic.get('data', [])
#	for data_dic in data_dic_ls:
#	    name = data_dic.get('name', '')
#	    if name:
#		print (name.encode('utf8'))
##	    print ('\t'.join(['\t', data_dic.get('name', '--'), data_dic.get('current_price', '--')]).encode('utf8'))

def parse_one_menu(ss, tb_name):
    ori_ss = jsonDecompress(ss)
    if ori_ss == ss:
	return None
    if 'meituan' in tb_name:
	parse_meituan_menu(ori_ss)
    elif 'eleme' in tb_name:
	parse_eleme_menu(ori_ss)
    elif 'baidu' in tb_name:
	parse_baidu_menu(ori_ss)

def test_parse_menu():
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_waimai')
    conn = mysql_obj['conn']
    cur = mysql_obj['cursor']
    tb_name0 = 'meituan_waimai_shop'
    tb_name1 = 'eleme_shop'
    tb_name2 = 'baidu_waimai_shop'
    for tb_name in [tb_name0, tb_name1, tb_name2]:
        sql = 'select `auto_id`, `menu` from `{}` where `menu` is not null limit 10000'.format(tb_name)
	cur.execute(sql)
	for res in cur.fetchall():
	    if not res:
		continue
    #       print (res['auto_id'])
            ss = res['menu']
    #       print ('ss', type(ss))
            parse_one_menu(ss, tb_name)

def test_menu_fusion():
    sql = "select menu from `{}` where id='{}'"
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_waimai')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']
    
    bd_parser = BdWmParser()
    mt_parser = MtWmParser()
    elm_parser = ElemeParser()
    
    menu_merger_obj = MenuMerger()
 
    tb_dic = {'eleme':'eleme_shop', 'baidu':'baidu_waimai_shop', 'meituan':'meituan_waimai_shop'}
    parser_dic = {'eleme':elm_parser, 'baidu':bd_parser, 'meituan':mt_parser}
    #for line in sys.stdin:
    for line in open('../data/res.out_json_offline', 'r'):
	dic = json.loads(line.strip())
	tup_ls = []
	for tag, _id in dic.items():
	    tb_name = tb_dic[tag]
	    cursor.execute(sql.format(tb_name, _id))
	    res = cursor.fetchone()
	    if res:
		parser = parser_dic[tag]
		menu = res['menu']
		ori_ls = parser.parse_one_menu(menu)
		name_ls = parser.get_all_food(ori_ls)
		if name_ls:
		    tup = (tag, name_ls)
		    tup_ls.append(tup)
	if len(tup_ls) > 1:
	    res_ls = menu_merger_obj.merge_menu_lists(tup_ls)
	    res_dic = {'shop_info':dic, 'food_info':res_ls}
	    print (json.dumps(res_dic, ensure_ascii=False).encode('utf8'))
	else:
	    res_ls = menu_merger_obj.merge_menu_lists(tup_ls)
	    res_dic = {'shop_info':dic, 'food_info':res_ls}
	    sys.stderr.write('{}\n'.format(json.dumps(res_dic, ensure_ascii=False).encode('utf8')))

def parse_specific_menu():
    sql = "select menu from `{}` where id='{}'"
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_waimai')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']
    sql = sql.format('eleme_shop', '66ab7e967c1de91a5f557cbb50d28958')
    cursor.execute(sql)
    dic = cursor.fetchone()
    menu = dic['menu']
    parse_one_menu(menu, 'eleme_shop')

def get_chaos_menu():
    sql = "select menu from `{}` where id='{}'"
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_waimai')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']
    
    bd_parser = BdWmParser()
    mt_parser = MtWmParser()
    elm_parser = ElemeParser()
    
    menu_merger_obj = MenuMerger()
 
    tb_dic = {'eleme':'eleme_shop', 'baidu':'baidu_waimai_shop', 'meituan':'meituan_waimai_shop'}
    parser_dic = {'eleme':elm_parser, 'baidu':bd_parser, 'meituan':mt_parser}
    ss = u'ð §§鸭腿'
    num = 0
    for line in open('../data/res.out_json_offline', 'r'):
	num += 1
	if num % 2000 == 0:
	    print (num)
	dic = json.loads(line.strip())
	tup_ls = []
	for tag, _id in dic.items():
	    tb_name = tb_dic[tag]
	    cursor.execute(sql.format(tb_name, _id))
	    res = cursor.fetchone()
	    if res:
		parser = parser_dic[tag]
		menu = res['menu']
		ori_ls = parser.parse_one_menu(menu)
		name_ls = parser.get_all_food(ori_ls)
		name_ls = set(name_ls)
		if ss in name_ls:
		    print (tag, _id)
		    sys.exit()
#		if name_ls:
#		    tup = (tag, name_ls)
#		    tup_ls.append(tup)
#	if len(tup_ls) > 1:
#	    res_ls = menu_merger_obj.merge_menu_lists(tup_ls)
#	    res_dic = {'shop_info':dic, 'food_info':res_ls}
#	    print (json.dumps(res_dic, ensure_ascii=False).encode('utf8'))
#	else:
#	    res_ls = menu_merger_obj.merge_menu_lists(tup_ls)
#	    res_dic = {'shop_info':dic, 'food_info':res_ls}
#	    sys.stderr.write('{}\n'.format(json.dumps(res_dic, ensure_ascii=False).encode('utf8')))


if __name__ == '__main__':
    #get_chaos_menu()
    #parse_specific_menu()
    test_menu_fusion()
