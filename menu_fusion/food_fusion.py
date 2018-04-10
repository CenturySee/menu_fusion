#!/usr/bin/python
# coding=utf8

import os
import sys
import json
import traceback

cur_dir = os.path.dirname(os.path.abspath(__file__))
proj_dir = os.sep.join([cur_dir, '..'])
conf_dir = os.sep.join([proj_dir, 'conf'])
utils_dir = os.sep.join([proj_dir, 'utils'])

key_name = 'name'
key_price = 'price'
key_image = 'image'
key_activity = 'activity'
key_source = 'source'
key_id = 'id'
key_foods = 'foods'
key_merge_info = 'merge_info'

def food_fusion(fn = 'merged_food.json'):
    '''
    进行菜品相关信息的合并
    input: fn string 聚好类的菜品 一行一个合并的店铺
    {
        foods:{
	       label:[
                       { food_from_source0 }, 
                       { food_from_source1 }, 
	   	       ...,
	   	     ]
	      }, 
        id:''
    }
    
    output: 打印结果 一行一个合并的店铺 
    {
	id:'', 
	foods:[
		{'name':{'baidu':"xxx", 'eleme':"xxx", 'meituan':"xxx"},  # 菜名
		 'price':{'baidu':xx, 'eleme':xx, 'meituan':xx},  # 当前价格
		 'image':{'baidu':"xxx", 'eleme':"xxx", 'meituan':"xxx"},  # 图片
		 'acitvity':{'baidu':"xxx", 'eleme':"xxx", 'meituan':"xxx"}  # 活动信息--限时五折等
		 }, ...
	],
	merge_info: {'baidu':{'id':""}, ...}
    }
    '''
    num = 0
    for line in open(fn, 'r'):
	dic = json.loads(line.strip())
	_id = dic['id']
	label_food_ls_dic = dic['foods']
	merged_food_ls = []
	merge_info = {}
	for label, food_ls in label_food_ls_dic.iteritems():
	    merged_food_dic = {key_name:{}, key_price:{}, \
		    key_image:{}, key_activity:{}}
	    for food_dic in food_ls:
		parsed_dic = parse_food_dic(food_dic)
		src = parsed_dic[key_source]
		__id = parsed_dic[key_id]
		if src not in merge_info:
		    merge_info[src] = {}
		    merge_info[src][key_id] = __id
		name = parsed_dic[key_name]
		price = parsed_dic[key_price]
		image = parsed_dic[key_image]
		activity = parsed_dic[key_activity]
		merged_food_dic[key_name][src] = name
		merged_food_dic[key_price][src] = price
		merged_food_dic[key_image][src] = image
		merged_food_dic[key_activity][src] = activity
	    if merged_food_dic:
		merged_food_ls.append(merged_food_dic)
	res_dic = {key_id:_id, key_foods:merged_food_ls, key_merge_info:merge_info}
	print (json.dumps(res_dic, ensure_ascii=False).encode('utf8'))
	num += 1
	

def parse_food_dic(food_dic):
    '''
    input: food_dic:
            {
                "__id": "0606616a3e597685be6e02ac335fac18",
                "__source": "baidu",
                ...
	    }
    output: dict
            {
	        "id": "",    # 来源的具体id
		"source": "",    # 来源 baidu eleme meituan
		"name": "",    # 菜品名称
		"price": "",    # 菜品当前价格
		"image": "",    # 菜品图片
		"activity": ""    # 活动信息
	    } 
    '''
    _id = food_dic['__id']
    source = food_dic['__source']
    name, price, image, activity = None, None, None, None
    if source == 'baidu':
	name = food_dic.get('name', None)
	price = food_dic.get('current_price', None)
	image = food_dic.get('url', None)
	activity = food_dic.get('dish_activity', None)
	activity = True if activity else False
    elif source == 'eleme':
	name = food_dic.get('name', None)
	specfoods = food_dic.get('specfoods', [])
	price = None
	for sp_dic in specfoods:
	    if sp_dic.get('name', '') == name:
	        price = sp_dic.get('price', None)
		break
	image = food_dic.get('image_path', None)
	activity = food_dic.get('activity', None)
	activity = True if activity else False
    elif source == 'meituan':
	name = food_dic.get('name', None)
	price = food_dic.get('min_price', None)
	image = food_dic.get('picture', None)
	activity = food_dic.get('activity_type', None)
	activity = True if activity else False
    res_dic = {key_name:name, key_price:price, \
	    key_image:image, key_activity:activity, \
	    key_source:source, key_id:_id}
    return res_dic


if __name__ == '__main__':
    food_fusion()
