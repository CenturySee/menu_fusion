#!/bin/usr/python
#encoding=utf8

import os
import sys
import json
import math
import time
import heapq
import random
import operator

import urllib
import hashlib
import requests

import jieba
jieba.dt.tmp_dir = './log/'

from collections import defaultdict

def sort_by_length():
    ls = []
    for line in sys.stdin:
	ln = line.strip()
	add = ln.replace('（', '(').replace('）', ')').lower()
	if add:
	    ls.append(add)
    ls = sorted(ls, key=lambda x:len(x))
    print ('\n'.join(ls))

def random_shuffle():
    ls = []
    for line in sys.stdin:
	ln = line.strip()
	ls.append(ln)
    random.shuffle(ls)
    print ('\n'.join(ls))

def random_sample():
    ls = []
    for line in sys.stdin:
	ln = line.strip()
	ls.append(ln)
    res_ls = random.sample(ls, 100)
    res_ls = sorted(res_ls, key=lambda x: len(x))
    print ('\n'.join(res_ls))

def get_parent_res():
    pass

def request_for_baidu(poi):
    #poi = (35.658651,139.745415)
    url_base = 'http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location={},{}&output=json&ak={}&sn={}'
    # 计算sn
    ak = 'RrCI6hHYzoDuQ8xQhtj1YLCcTW1GAa4F'
    sk = 'EViz0M6gsge2l8lty1FELSuZ5wjmmRou'
    query_str = '/geocoder/v2/?callback=renderReverse&location={},{}&output=json&ak={}'
    query_str = query_str.format(poi[0], poi[1], ak)
    encoded_str = urllib.quote(query_str, safe="/:=&?#+!$,;'@()*[]")
    raw_str = encoded_str + sk
    sn = hashlib.md5(urllib.quote_plus(raw_str)).hexdigest()
    url = url_base.format(poi[0], poi[1], ak, sn)
    # 进行请求
    r = requests.get(url)
    json_str = r.text.strip('renderReverse&&renderReverse').strip('(').strip(')')
    dic = json.loads(json_str)
    return dic
#    print json.dumps(dic, ensure_ascii=False)
   
def compute_address():
    poi_set = set()
    num = 0
    for line in sys.stdin:
	ln = line.strip().decode('utf8')
	ls = ln.split()
	poi = tuple(ls[0].split(','))
	if poi not in poi_set:
	    dic = request_for_baidu(poi)
	    if dic['status'] == 0:
		dic['waimai_address'] = ls[-1]
		print json.dumps(dic, ensure_ascii=False).encode('utf8')
	    num += 1
	    if num % 3000 == 0:
		time.sleep(59)
	    if num >= 6000:
		return

def jieba_cut():
    '''
    进行结巴分词
    '''
    for line in sys.stdin:
	ln = line.strip()
	print ' '.join(jieba.cut(ln)).encode('utf8')

def get_word_stat():
    '''
    统计分词效果的词频等信息
    结果存储到文件中 word_stat.json
    '''
    # 计算每个词的左右频率
    word_lr_dic = defaultdict(lambda :defaultdict(lambda: defaultdict(int)))
    word_cnt_dic = defaultdict(int)
    for line in sys.stdin:
	ln = line.decode('utf8').strip()
	ls = ln.split()
	if len(ls) == 1:
	    word_cnt_dic[ls[0]] += 1
	elif len(ls) > 1:
	    b, e = ls[0], ls[-1]
	    word_lr_dic[b]['r'][e] += 1
	    word_cnt_dic[b] += 1
	    word_cnt_dic[e] += 1
	    word_lr_dic[e]['l'][b] += 1
	    for ii, ss in enumerate(ls[1:-1], 1):
		sl, sr = ls[ii-1], ls[ii+1]
		word_lr_dic[ss]['l'][sl] += 1
		word_lr_dic[ss]['r'][sr] += 1
		word_cnt_dic[ss] += 1
    print (json.dumps(word_lr_dic, ensure_ascii=False).encode('utf8'))
    print (json.dumps(word_cnt_dic, ensure_ascii=False).encode('utf8'))

def load_word_stat(fn='word_stat.json'):
    '''
    加载词统计信息
    '''
    ls = []
    for line in open(fn, 'r'):
	ln = line.strip()
	dic = json.loads(ln)
	ls.append(dic)
    return ls

def compute_all_entropy():
    '''
    进行左右熵的计算 输出字数少且左右熵top50的词
    '''
    # 加载词频统计信息
    tup = load_word_stat()
    word_lr_dic, word_cnt_dic = tup
    # 计算bigram的总数
    bi_denom = 0
    for k, v_dic in word_lr_dic.iteritems():
	bi_denom += sum(v_dic.get('l', {}).values())
	bi_denom += sum(v_dic.get('r', {}).values())
    print ('bi_denom', bi_denom)
    bi_denom /= 2
    # 筛选出字数少的词
    key_dic = {}
    for k, v in word_lr_dic.iteritems():
	if len(k) < 3:
	    key_dic[k] = v
    # 计算出现10次以上的词的左右熵
    cnt_thred = 10
    l_entropy_dic = {}
    r_entropy_dic = {}
    for w, lr_cnt_dic in key_dic.iteritems():
	if word_cnt_dic[w] <= cnt_thred:
	    continue
	w_cnt = word_cnt_dic[w]
	# 计算左信息熵
	l_dic = lr_cnt_dic.get('l', {})
	if l_dic:
	    l_entropy = compute_single_entropy(l_dic)
	    l_entropy_dic[w] = (l_entropy, w_cnt)
	# 计算右信息熵
	r_dic = lr_cnt_dic.get('r', {})
	if r_dic:
	    r_entropy = compute_single_entropy(r_dic)
	    r_entropy_dic[w] = (r_entropy, w_cnt)
    # 对信息熵进行排序
    topn = 5
    l_entropy_ls = sorted(l_entropy_dic.items(), key=lambda x:(x[1][0], -x[1][1]))
    for tup_ls in l_entropy_ls[:topn]:
	word = tup_ls[0]
	compute_compactness(word, word_lr_dic[word]['l'], word_cnt_dic, bi_denom)

def compute_single_entropy(l_dic):
    '''
    计算左右熵
    输入: l_dic {key_word: word_cnt}
    输出: 信息熵
    '''
    ls = list(l_dic.values())
    denom = sum(ls)
    entropy = 0.0
    for cnt in ls:
	freq = 1.0*cnt/denom 
	entropy += -1 * freq * math.log(freq)
    return entropy

def compute_compactness(word, l_cnt_dic, word_cnt_dic, bi_denom):
    denom = sum(word_cnt_dic.values())
    print ('denom', denom)
    w_cnt = word_cnt_dic[word]
    res_dic = {}
    for lw, cnt in l_cnt_dic.iteritems():
	l_cnt = word_cnt_dic[lw]
	lc_cnt = cnt
	res_dic[lw+' '+word] = (1.0*lc_cnt*denom*denom/l_cnt/w_cnt/bi_denom, lc_cnt, l_cnt, w_cnt)
#    topn = 50
    topn_ls = sorted(res_dic.items(), key=lambda x:(x[1][0],x[1][1],x[1][2],x[1][3]), reverse=True)
    topn_ls = filter(lambda x:x[1][0] > 1000, topn_ls)
    for tup in topn_ls:
	print (json.dumps(tup, ensure_ascii=False).encode('utf8'))


if __name__ == '__main__':
#    random_shuffle()
#    get_word_stat()
    compute_all_entropy()
#    jieba_cut()
#    compute_address()
#    random_sample()
#    sort_by_length()
