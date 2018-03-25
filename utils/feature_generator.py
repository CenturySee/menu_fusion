#!/usr/bin/python
#encoding=utf8

from str_normalizer import StringNormalizer
from eleme_parser import ElemeParser
from meituan_waimai_parser import MtWmParser
from baidu_waimai_parser import BdWmParser

class FeatureGenerator():
    def __init__(self):
        self.normalizer = StringNormalizer()
	self.elem_parser = ElemeParser()
	self.meituan_parser = MtWmParser()
	self.baidu_parser = BdWmParser()
	pass

    def generate_feature(self, sql_dic, src):
	'''
	特征生成
	input: sql_dic  从mysql中取出的一条记录
	output: feature_ls  该记录中菜品对应的特征 
	        [[src, id, brand_name, food, norm_food], [...]]
		src:来源    id:店ID    brand_name:店名    food:菜品名称    norm_food:归一化菜品名
	'''
	_id = sql_dic.get('id', '')
	brand_name = sql_dic.get('s_brand_name', '')
	menu = sql_dic.get('menu', '')
	parser = None
	if 'eleme' in src:
	    parser = self.elem_parser
	elif 'meituan' in src:
	    parser = self.meituan_parser
	elif 'baidu' in src:
	    parser = self.baidu_parser
	food_ls = []
	if parser:
	    food_ls = parser.get_all_food_from_menu(menu)
	res_ls = []
	for food in food_ls:
	    norm_food = self.normalizer.normalize(food)
	    res_ls.append([src, _id, brand_name, food, norm_food])
	return res_ls

def test_feature_generator():
    feat_gen = FeatureGenerator()

if __name__ == '__main__':
    test_feature_generator()
