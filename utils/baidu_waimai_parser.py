#!/usr/bin/python
# coding=utf8

from directory_info import *

class BdWmParser():
    def __init__(self):
	pass

    def parse_one_menu(self, menu):
	'''
	获取菜单的原始数据
	'''
	if not menu:
	    return None
	ori_ss = jsonDecompress(menu)
        ori_ss = json.loads(ori_ss)
	if isinstance(ori_ss, dict):
	    ori_ss = list(ori_ss.values())
	return ori_ss

    def get_all_food(self, ori_ss):
	name_set = set()
	if not ori_ss:
	    return []
	id_name_dic = {}
	for base_dic in ori_ss:
	    catalog = base_dic.get('catalog', '--')  # 类目信息 如：时令超值套餐
	    datas = base_dic.get('data', [])  # 获取类目下的菜品列表
	    for data_dic in datas:
	        name = data_dic.get('name', '')  # 菜品名称
		_id = data_dic.get('item_id', '')  # 菜品ID
		if _id and name:
		    id_name_dic[_id] = name
		    name_set.add(name)
	return list(name_set)
    
    def get_all_food_from_menu(self, ori_ss):
	dic_ls = self.parse_one_menu(ori_ss)
	food_ls = self.get_all_food(dic_ls)
	return food_ls


def test_bdwm_parse():
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_waimai')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']
    sql = "select menu from `{}` where out_id='{}'"
    tup3 = ('baidu_waimai_shop', '1432867840')
    tb_name, _id = tup3
    cursor.execute(sql.format(tb_name, _id))
    res = cursor.fetchone()
    if res:
	wm_parser = BdWmParser()
        menu = res['menu']
	ori_ss = wm_parser.parse_one_menu(menu)
	name_ls = wm_parser.get_all_food(ori_ss)
	print (json.dumps(name_ls, ensure_ascii=False))

if __name__ == '__main__':
    test_bdwm_parse()
