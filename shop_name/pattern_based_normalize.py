#!/usr/bin/python
#coding=utf8

import os
import re
import sys
import json

LTP_DATA_DIR = "/Users/Zhenqi.Xu/Downloads/open_source/LTP/ltp_data_v3.4.0"
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, 'segment.lexicon')  # 加载模型

from pyltp import Postagger
postagger = Postagger() # 初始化实例
postagger.load_with_lexicon(pos_model_path, 'postag.lexicon')  # 加载模型

from pyltp import NamedEntityRecognizer
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(ner_model_path)  # 加载模型

from pyltp import Parser
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型

def process_segment_lexicon():
    suffix = re.compile("(分店|店|站|路|街)$")
    for line in open('brand.res', 'r'):
        ln = ''.join(line.strip().split())
        if ln:
            print (ln)
    for line in open('branch.res', 'r'):
        ln = ''.join(line.strip().split())
        if ln:
            print (ln)
        ln1 = suffix.sub('', ln)
        if ln != ln1 and ln1:
            print (ln1)

def process_postag_lexicon():
    suffix = re.compile("(分店|店|站|路|街)$")
    for line in open('brand.res', 'r'):
        ln = ''.join(line.strip().split())
        if ln:
            print (' '.join([ln, 'ni']))
    for line in open('branch.res', 'r'):
        ln = ''.join(line.strip().split())
        if ln:
            print (' '.join([ln, 'ns']))
        ln1 = suffix.sub('', ln)
        if ln != ln1 and ln1:
            print (' '.join([ln1, 'ns']))

def process_one_shop(shop):
    shop = ''.join(shop.strip().split())
    words = segmentor.segment(shop)
    postags = postagger.postag(words)
    netags = recognizer.recognize(words, postags)
    arcs = parser.parse(words, postags)  # 句法分析
    print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
    res_dic = {'words':list(words), 'postags':list(postags), 'netags':list(netags)}
    print (json.dumps(res_dic, ensure_ascii=False))

def process_auto_shop_name():
    for line in sys.stdin:
        ln = line.strip()
        dic = json.loads(ln)
        shop = ''.join(dic['shop'].strip().split()).encode('utf8')
        words = segmentor.segment(shop)
        postags = postagger.postag(words)
        netags = recognizer.recognize(words, postags)
        res_dic = {'words':list(words), 'postags':list(postags), 'netags':list(netags)}
        print (json.dumps(res_dic, ensure_ascii=False))

pat_dic = {'brand_tag':['ni'], 'branch_tag':['ns'], 'dependency':['ATT']}
def pattern_based_normalize(shop, pat_dic = pat_dic):
    tag0s = pat_dic['brand_tag']
    tag1s = pat_dic['branch_tag']
    deps = pat_dic['dependency']
    shop = ''.join(shop.strip().split()).encode('utf8')
    words = segmentor.segment(shop)
    word_ls = list(words)
    postags = postagger.postag(words)
    postag_ls = list(postags)
    arcs = parser.parse(words, postags)  # 句法分析
    arc_tup_ls = [(arc.head, arc.relation) for arc in arcs]
    branch, brand = None, None
    for ii, tag in enumerate(postag_ls):
        if tag in tag0s:
            dst_ind, dep_i = arc_tup_ls[ii]
            if dep_i in deps and postag_ls[dst_ind-1] in tag1s:
                brand = word_ls[ii]
                branch = word_ls[dst_ind-1]
                break
    res_dic = {'brand':brand, 'branch':branch, 'shop':shop}
    return res_dic

def pattern_based_normalize_batch():
    for line in sys.stdin:
        ln = line.strip()
        dic = json.loads(ln)
        shop = dic['shop']
        res_dic = pattern_based_normalize(shop)
        brand = res_dic.get('brand', '')
        branch = res_dic.get('branch', '')
        if brand and branch:
            print (json.dumps(res_dic, ensure_ascii=False))
        else:
            sys.stderr.write('{}\n'.format(json.dumps(res_dic, ensure_ascii=False)))

if __name__ == "__main__":
    #process_segment_lexicon()
    #process_postag_lexicon()
    #process_auto_shop_name()
    #ss = u'北京麦当劳学院路餐厅'
    #ss = '上海麦当劳沪宜DT餐厅'
    #ss = '快乐丸家（21世纪太阳城）'
    #ss = '上海麦当劳丰庄餐厅'
    #process_one_shop(ss)
    #res_dic = pattern_based_normalize(ss)
    #print (json.dumps(res_dic, ensure_ascii=False))
    pattern_based_normalize_batch()