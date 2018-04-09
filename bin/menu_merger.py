#!/usr/bin/python
#encoding=utf8
import sys
from collections import defaultdict

sys.path.append('../utils/')
from directory_info import *
from str_normalizer import StringNormalizer

class MenuMerger():
    def __init__(self):
        self.norm_obj = StringNormalizer()
        pass

    def merge_menu_lists(self, tup_ls):
	'''
	merge menus from different source
	input: tup_ls  [(tag, food_set), (tag, food_set), ...]
	output: res_dic  {normalize_food:[source0, source1,..], ...}
	'''
        set_ls = list([set([self.norm_obj.normalize(ss) for ss in tup[1]]) for tup in tup_ls])
	tag_ls = list([tup[0] for tup in tup_ls])
	all_set = set()
	for seti in set_ls:
	    all_set.update(seti)
	res_dic = defaultdict(list)
	for ss in all_set:
	    for tagi, seti in zip(tag_ls, set_ls):
		if ss in seti:
		    res_dic[ss].append(tagi)
	return res_dic


def test_menu_merge():
    t0 = '0'
    ls0 = [u'你好123Nihao', u'你好']
    t1 = '1'
    ls1 = [u'你好123nihao', u'  你 好 ']
    tup_ls = [(t0, ls0), (t1, ls1)]
    menu_merger_obj = MenuMerger()
    res_dic = menu_merger_obj.merge_menu_lists(tup_ls[:1])
    print (json.dumps(res_dic, ensure_ascii=False))

if __name__ == '__main__':
    test_menu_merge()
