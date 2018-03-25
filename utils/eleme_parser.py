#!/usr/bin/python
# coding=utf8

from directory_info import *

class ElemeParser():
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
        ori_ss = json.loads(ori_ss)
	return ori_ss

    def get_all_food(self, ori_ss):
	name_set = set()
	if not ori_ss:
	    return []
	id_name_dic = {}
	for base_dic in ori_ss:
	    name = base_dic.get('name', '--')  # 类目信息 如：时令超值套餐
	    foods = base_dic.get('foods', [])  # 获取类目下的菜品列表
	    for food_dic in foods:
		specfoods = food_dic.get('specfoods', [])  # 相同菜品的不同规格 如：请备注选炖汤：（虫草花肉汁、雪梨雪耳炖猪肺、无花果排骨），无备注随机配汤
	        name = food_dic.get('name', '')  # 菜品名称
		_id = food_dic.get('item_id', '')  # 菜品ID
		if _id and name:
		    id_name_dic[_id] = name
		    name_set.add(name)
	return list(name_set)
    
    def get_all_food_from_menu(self, ori_ss):
	dic_ls = self.parse_one_menu(ori_ss)
	food_ls = self.get_all_food(dic_ls)
	return food_ls


def test_elem_parse():
    mysql_obj = get_mysql_obj(os.sep.join([conf_dir, 'db.conf']), 'mysql_waimai')
    conn = mysql_obj['conn']
    cursor = mysql_obj['cursor']
    sql = "select menu from `{}` where id='{}'"
    tup3 = ('eleme_shop', '0c9b9ea9aa6b5754519976a53f3c9554')
    tb_name, _id = tup3
    cursor.execute(sql.format(tb_name, _id))
    res = cursor.fetchone()
    if res:
	elem_parser = ElemeParser()
        menu = res['menu']
	ori_ss = elem_parser.parse_one_menu(menu)
	name_ls = elem_parser.get_all_food(ori_ss)
	print (json.dumps(name_ls, ensure_ascii=False))

if __name__ == '__main__':
    test_elem_parse()
