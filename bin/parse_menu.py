#!/usr/bin/python
#coding=utf8

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

def get_sample_shop_from_sample_file():
    '''
    通过采样文件获取同一商家在不同app中的id
    输入: sys.stdin
<<<<<<< HEAD
    720e49b2f4c6991ff4b3b6500fd815ba        1        印象柳螺柳州螺蛳粉•匠心制造        waimai
    meituan_id        cnt brand_name        type
    输出: sys.stdout
    meituan_id        cnt brand_name        meituan_id  eleme_id  baidu_id
=======
    720e49b2f4c6991ff4b3b6500fd815ba	1	印象柳螺柳州螺蛳粉•匠心制造	waimai
    meituan_id	cnt brand_name	type
    输出: sys.stdout
    meituan_id	cnt brand_name	meituan_id  eleme_id  baidu_id
>>>>>>> 4cca5f0e4264c66366b590f7a182ce39f800a3b1
    '''
    sql = "select * from `std_shop` where id='{}' limit 1"
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_waimai')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']
    for line in sys.stdin:
<<<<<<< HEAD
        ln = line.strip()
        ls = ln.split('\t')
        _id, cnt, name, typ = ls
        cursor.execute(sql.format(_id))
        dic = cursor.fetchone()
        if not dic:
            sys.stderr.write('has no such id: {}\n'.format(_id))
            continue
        merge_info_str = dic.get('merge_info', '')
        if not merge_info_str:
            sys.stderr.write('has not merge_info, id: {}\n'.format(_id))
            continue
        merge_info = json.loads(merge_info_str)
        m_id = merge_info.get('meituan_waimai', {}).get('out_id', '')
        e_id = merge_info.get('eleme', {}).get('out_id', '')
        b_id = merge_info.get('baidu_waimai', {}).get('out_id', '')
        id_ls = []
        if m_id: id_ls.append(m_id)
        if e_id: id_ls.append(e_id)
        if b_id: id_ls.append(b_id)
        if len(id_ls) < 2:
            sys.stderr.write('only has one source, id: {}\n'.format(_id))
            continue
        tmp_out_ls = [_id, cnt, name, m_id, e_id, b_id]
        out_ls = []
        for ss in tmp_out_ls:
            if not isinstance(ss, str):
                ss = ss.encode('utf8')
            out_ls.append(ss)
        print ('\t'.join(out_ls))
=======
	ln = line.strip()
	ls = ln.split('\t')
	_id, cnt, name, typ = ls
	cursor.execute(sql.format(_id))
	dic = cursor.fetchone()
	if not dic:
	    sys.stderr.write('has no such id: {}\n'.format(_id))
	    continue
	merge_info_str = dic.get('merge_info', '')
	if not merge_info_str:
	    sys.stderr.write('has not merge_info, id: {}\n'.format(_id))
	    continue
	merge_info = json.loads(merge_info_str)
	m_id = merge_info.get('meituan_waimai', {}).get('out_id', '')
	e_id = merge_info.get('eleme', {}).get('out_id', '')
	b_id = merge_info.get('baidu_waimai', {}).get('out_id', '')
	id_ls = []
	if m_id: id_ls.append(m_id)
	if e_id: id_ls.append(e_id)
	if b_id: id_ls.append(b_id)
	if len(id_ls) < 2:
	    sys.stderr.write('only has one source, id: {}\n'.format(_id))
	    continue
	tmp_out_ls = [_id, cnt, name, m_id, e_id, b_id]
	out_ls = []
	for ss in tmp_out_ls:
	    if not isinstance(ss, str):
		ss = ss.encode('utf8')
	    out_ls.append(ss)
	print ('\t'.join(out_ls))
>>>>>>> 4cca5f0e4264c66366b590f7a182ce39f800a3b1
    
 
# 通过采样的样本获取菜品特征 用来标注
def get_unlabeled_data():
    '''
    input: sys.stdin
    output: sys.stdout  \t split  id shop_name food_name mid eid bid
    '''
    sql = "select * from `{}` where id='{}'"
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_online')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']
    
    bd_parser = BdWmParser()
    mt_parser = MtWmParser()
    elm_parser = ElemeParser()
 
    tb_dic = {'eleme':'eleme_shop', 'baidu':'baidu_waimai_shop', 'meituan':'meituan_waimai_shop'}
    tb_ls = ['meituan_waimai_shop', 'eleme_shop', 'baidu_waimai_shop']
    parser_ls = [mt_parser, elm_parser, bd_parser]
    id_set = set()
    for line in sys.stdin:
        ls = line.strip().split('\t')
        try:
            _id, cnt, name, typ, city, m_id, e_id, b_id = ls
        except:
            continue
        if _id in id_set:
            continue
        id_set.add(_id)
        for a_id, tb, parser in zip([m_id, e_id, b_id], tb_ls, parser_ls):
            if not a_id:
                continue
            sql_i = sql.format(tb, a_id)
            cursor.execute(sql_i)
            dic = cursor.fetchone()
            food_ls = parser.get_all_food_from_menu(dic.get('menu', ''))
            for food in food_ls:
                str_ls = [_id, name, typ, city, food.encode('utf8'), a_id, tb]
                #str_ls = [ss.encode('utf8') for ss in str_ls]
                print ('\t'.join(str_ls))
        print ('')
        if len(id_set) >=50:
            break
        

def parse_specific_menu():
    bd_parser = BdWmParser()
    mt_parser = MtWmParser()
    elm_parser = ElemeParser()
    src_tb_dic = {'baidu':'baidu_waimai_shop', 'meituan':'meituan_waimai_shop', 'eleme':'eleme_shop'}
    tb_parser_dic = {'baidu_waimai_shop':bd_parser, 'meituan_waimai_shop':mt_parser, 'eleme_shop':elm_parser}
    
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_online')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']

    for line in sys.stdin:
        ln = line.strip()
        dic = json.loads(ln)
        for src, _id in dic.items():
            src_tb = src_tb_dic[src]
            parser = tb_parser_dic[src_tb]
            sql = "select menu from `{}` where id='{}' limit 1"
            sql = sql.format(src_tb, _id) 
            cursor.execute(sql)
	    dic = cursor.fetchone()
            menu = dic.get('menu', '')
            menu_ls = parser.parse_one_menu(menu)
            print (json.dumps(menu_ls, ensure_ascii=False).encode('utf8'))
        sys.exit()

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
#                if name_ls:
#                    tup = (tag, name_ls)
#                    tup_ls.append(tup)
#        if len(tup_ls) > 1:
#            res_ls = menu_merger_obj.merge_menu_lists(tup_ls)
#            res_dic = {'shop_info':dic, 'food_info':res_ls}
#            print (json.dumps(res_dic, ensure_ascii=False).encode('utf8'))
#        else:
#            res_ls = menu_merger_obj.merge_menu_lists(tup_ls)
#            res_dic = {'shop_info':dic, 'food_info':res_ls}
#            sys.stderr.write('{}\n'.format(json.dumps(res_dic, ensure_ascii=False).encode('utf8')))


if __name__ == '__main__':
    #get_sample_shop_from_sample_file()
    #get_unlabeled_data()
    #get_chaos_menu()
    parse_specific_menu()
    #test_menu_fusion()
