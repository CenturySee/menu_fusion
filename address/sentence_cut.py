#!/bin/python
#coding=utf8

'''
获取人工标注的数据
'''

import os
import sys
import json
import math
import time
import heapq
import random
import logging
import operator
import traceback
from collections import defaultdict
#from bson import json_util

cur_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = cur_dir # os.path.sep.join([cur_dir, '..', '..'])

utils_dir = os.path.sep.join([base_dir, 'utils'])
sys.path.append(utils_dir)

LTP_DATA_DIR = os.sep.join([base_dir, 'ltp_data'])
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型

from pyltp import Postagger
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型

from pyltp import NamedEntityRecognizer
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(ner_model_path)  # 加载模型

def parse_one_sentence(sentence):
	words = segmentor.segment(sentence)
	postags = postagger.postag(words)
	netags = recognizer.recognize(words, postags)
	res_dic = {'words':list(words), 'postags':list(postags), 'netags':list(netags)}
	return res_dic

def parse_all_sentence():
	for line in sys.stdin:
		ln = line.strip()
		ln = ln.replace('（', '(').replace('）', ')').lower()
		res_dic = parse_one_sentence(ln)
		print json.dumps(res_dic, ensure_ascii=False)

def test_parse_one_sentence(sentence):
	sentence = '北京市朝阳区北辰世纪中心A座'
	res_dic = parse_one_sentence(sentence)
	print json.dumps(res_dic, ensure_ascii=False)

def sample_cut_result():
	ls_ls = []
	for line in open('meb.cut', 'r'):
		ln = line.strip().decode('utf8')
		dic = json.loads(ln)
		word_ls = dic['words']
		ls_ls.append(word_ls)
	out_ls = random.sample(ls_ls, 500)
	for words in out_ls:
		print (' '.join(words).encode('utf8'))

def get_all_number_suffix():
	suffix_dic = defaultdict(int)
	prefix_dic = defaultdict(int)
	for line in open('meb.ltp_cut', 'r'):
		ln = line.strip().decode('utf8')
		dic = json.loads(ln)
		words = dic['words']
		postags = dic['postags']
		length = len(postags)
		for ii, postag in enumerate(postags):
			if postag == 'm':
				if ii - 1 > 0:
					word = words[ii-1]
					prefix_dic[word] += 1
				if ii + 1 < length:
					word = words[ii+1]
					suffix_dic[word] += 1
	top_num = 50
	func = lambda x: x[1]
	suffix_tup_ls = heapq.nlargest(top_num, suffix_dic.iteritems(), func)
	print ('suffix:')
	for tup in suffix_tup_ls:
		print (json.dumps(tup, ensure_ascii=False))
	print ('prefix:')
	prefix_tup_ls = heapq.nlargest(top_num, prefix_dic.iteritems(), func)
	for tup in prefix_tup_ls:
		print (json.dumps(tup, ensure_ascii=False))

if __name__ == '__main__':
	get_all_number_suffix()
	#sample_cut_result()
	#parse_all_sentence()
