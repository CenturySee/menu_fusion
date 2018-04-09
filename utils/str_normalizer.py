#!/usr/bin/python
#encoding=utf8

import os, re, sys, json
from hanziconv import HanziConv

class StringNormalizer():
	def __init__(self):
		self.spec_dic = { \
		u'＋':u'+', u'&':u'+', u'➕':u'+', u'十':u'+', \
		u'【':u'[', u'◥':u'[', u'】':u']', u'◤':u']', \
		u'”':u'"', u'“':u'"', u"'":u'"', \
		u'（':u'(', u'）':u')', u'：':u':', u'／':u'/' \
		}
	self.char_filter = re.compile(u'[^\u4E00-\u9FA5A-Za-z0-9]') # 过滤出中文 字母 数字 其余符号用空格表示
	pass

    def strip(self, ss):
	if ss:
	    return ''.join(ss.strip().split())

    def tradition2simple(self, ss):
	'''
	中文繁简转换
	'''
	pass

    def filter_character(self, string):
	'''
	过滤出中文 字母 数字 下划线 其余符号用空格表示
	'''
	pass


    def normalize(self, ss):
	# 繁简转换
	ss1 = HanziConv.toSimplified(ss)
	# 大小写转换
	ss2 = ss1.lower()
	# 过滤出 中文 字母 数字 其余字符用空格表示
	ss3 = self.char_filter.sub(r' ', ss2)
	# 多个空格合并
	ss4 = ' '.join(ss3.strip().split())
	if not isinstance(ss4, str):
	    ss4 = ss4.encode('utf8')
	return ss4
#	# 归一化空格
#	ss = ''.join(ss.strip().split())
#	# 去除字符串最后的 ...  。❤  ! .
#	ss = ss.strip(u'。❤!！.°')
#	# 归一化字母
#	ss = ss.lower()
#	# 归一化特殊字符: / [ ]
#	new_ss = ''
#	for s in ss:
#		new_ss += self.spec_dic.get(s, s)
#	return new_ss

if __name__ == '__main__':
	str_norm_obj = StringNormalizer()
	ss = u'i【  ◥  ＋  &  ➕ 十...  。❤  ! .  '
	print str_norm_obj.normalize(ss)
