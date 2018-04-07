#!/usr/bin/python
#coding=utf8

import os
import re
import sys
import json

from hanziconv import HanziConv

class ShopNameNormalizer():
    '''
    店名归一化
    '''
    def __init__(self):
        self.bracket_pat = re.compile(u'\((.*?)\)')
        self.branch_dict = {}   # 分支机构名称
        self.brand_dict = {}    # 店名名称
        self.suffix = re.compile(u"分店|店|站|路|街$")
        self.__init = False
        pass

    def load_branch_name(self, fn):
        for line in open(fn, 'r'):
            ln = line.strip().decode('utf8')
            self.branch_dict[ln] = ln
            ln1 = self.suffix.sub('', ln)
            self.branch_dict[ln1] = ln

    def load_brand_name(self, fn):
        for line in open(fn, 'r'):
            ln = line.strip().decode('utf8')
            self.brand_dict[ln] = ln

    def init_all(self, brand_fn='brand.res', branch_fn='branch.res'):
        if not self.__init:
            self.load_branch_name(brand_fn)
            self.load_brand_name(branch_fn)
            self.__init = True

    def split_shop_name(self, ss):
        '''
        进行单个店铺名称的解析
        :param ss: srting 原始店铺名称
        :return: dict 括号中的内容列表  剩余字符串的列表
        '''
        if isinstance(ss, str):
            ss = ss.decode('utf8')
        # 简繁转换
        ss = HanziConv.toSimplified(ss)
        # 大小写转换
        ss = ss.lower()
        # 括号转换
        ss = ss.strip().replace(u'（', '(').replace(u'）',')')
        ss = re.sub('\(+', '(', ss)
        ss = re.sub('\)+', ')', ss)
        # 可能需要验证是否有其他特殊符号存在(20180403)
        bracket_res_ls = re.findall(self.bracket_pat, ss)
        res_str = ss
        if bracket_res_ls:
            for s in bracket_res_ls:
                res_str = res_str.replace('('+ s +')', '####asdf####')
        remain_res_ls = res_str.split('####asdf####')
        remain_res_ls = [s for s in remain_res_ls if s]
        res_dic = {'bracket':bracket_res_ls, 'remain':remain_res_ls}
        return res_dic

    def __parse_brand(self, bracket_ls, remain_ls):
        '''
        解析品牌名称
        :param bracket_ls: 括号中的内容
        :param remain_ls: 剩余的内容
        :return: brand: string
        '''
        bracket_ls = list(set(bracket_ls))
        remain_ls = list(set(remain_ls))
        bracket_length = len(bracket_ls)
        brand = None
        if bracket_length == 1:
            branch = self.__parse_branch(bracket_ls)
            if branch:
                if len(remain_ls) == 1:
                    brand = remain_ls[0]
        return brand

    def parse_brand(self, shop_name):
        '''
        解析品牌名称
        :param shop_name: string 原始店铺名称
        :return: brand: string 品牌名称
        '''
        brand = None
        if shop_name:
            split_dic = self.split_shop_name(shop_name)
            bracket_ls, remain_ls = split_dic['bracket'], split_dic['remain']
            brand = self.__parse_brand(bracket_ls, remain_ls)
            if not brand:
                brand = self.__parse_brand(remain_ls, bracket_ls)
        return brand

    def parse_brand_from_file(self, shop_fn):
        '''
        进行店铺名称的批量识别
        :return: None
        '''
        if not self.__init:
            self.init_all()
        for line in open(shop_fn, 'r'):
            ln = line.strip()
            brand = self.parse_brand(ln)
            if brand:
                print (brand.encode('utf8'))
            else:
                sys.stderr.write('{}\n'.format(ln))

    def get_cand_branch_with_specific_suffix(self, ss):
        '''
        获取特定后缀的分支名
        :param ss: 候选分支名称
        :return:
        '''
        ss = ss.strip()
        if isinstance(ss, str):
            ss = ss.decode('utf8')
        if ss and re.search(self.suffix, ss):
            return ss
        else:
            return None

    def __parse_branch(self, bracket_ls):
        '''
        解析疑似分支机构名称
        :param bracket_ls: 括号内内容列表
        :return: 结构化的分支结构名称
        '''
        branch = None
        bracket_ls = list(set(bracket_ls))
        if len(bracket_ls) == 1:
            branch = bracket_ls[0]
            if branch in self.branch_dict:
                branch = self.branch_dict[branch]
            else:
                branch = self.get_cand_branch_with_specific_suffix(branch)
        return branch

    def parse_branch(self, shop_name):
        '''
        解析品牌名称
        :param shop_name: string 原始店铺名称
        :return: branch: string 分支名称
        '''
        branch = None
        if shop_name:
            split_dic = self.split_shop_name(shop_name)
            bracket_ls, remain_ls = split_dic['bracket'], split_dic['remain']
            branch = self.__parse_branch(bracket_ls)
            if not branch:
                branch = self.__parse_branch(remain_ls)
        return branch

    def parse_branch_from_file(self, shop_fn):
        '''
        进行店铺名称的批量识别
        :return: None
        '''
        if not self.__init:
            self.init_all()
        for line in open(shop_fn, 'r'):
            ln = line.strip()
            branch = self.parse_branch(ln)
            if branch:
                print (branch.encode('utf8'))
            else:
                sys.stderr.write('{}\n'.format(ln))


    def __parse_brand_and_branch(self, bracket_ls, remain_ls):
        '''
        分支机构 店名 解析
        :param : bracket_ls: 括号中的字符
        :param : remain_ls: 剩余的字符  parse_shop_name的输出
        :return: res_dic: dict {branch:'', brand:''}
        '''
        bracket_ls = list(set(bracket_ls))
        remain_ls = list(set(remain_ls))
        bracket_length = len(bracket_ls)
        branch_name = None
        brand_name = None
        if bracket_length == 1:
            norm_res = self.__parse_branch(bracket_ls)
            if norm_res:
                branch_name = norm_res
                brand_name = '##'.join(remain_ls)
            else:
                if len(remain_ls) == 1 and remain_ls[0] in self.brand_dict:
                    shop_name = self.brand_dict[remain_ls[0]]
                    if len(bracket_ls) == 1:
                        branch_name = bracket_ls[0]
        res_dic = {'branch':branch_name, 'brand':brand_name}
        return res_dic

    def parse_brand_and_branch(self, shop_name):
        '''
        进行分支结构 + 店名的解析
        :param shop_name: string 店名的全称
        :return: res_dic: dict {branch:'', brand:'', shop:''}
        '''
        if not self.__init:
            self.init_all()
        split_dic = self.split_shop_name(shop_name)
        remain_ls, bracket_ls = split_dic['remain'], split_dic['bracket']
        res_dic = self.__parse_brand_and_branch(bracket_ls, remain_ls)
        brand = res_dic['brand']
        branch = res_dic['branch']
        if brand and branch:
            res_dic['shop'] = shop_name
        else:
            res_dic = self.__parse_brand_and_branch(remain_ls, bracket_ls)
            res_dic['shop'] = shop_name
            brand = res_dic['brand']
            branch = res_dic['branch']
            if not brand or not branch:
                res_dic['brand'] = shop_name
                res_dic['branch'] = None
        return res_dic

    def parse_brand_and_branch_from_file(self, shop_fn):
        '''
        进行店铺名称的批量识别
        :return: None
        '''
        if not self.__init:
            self.init_all()
        for line in open(shop_fn, 'r'):
            ln = line.strip().decode('utf8')
            if ln:
                res_dic = self.parse_brand_and_branch(ln)
                brand, branch = res_dic['brand'], res_dic['branch']
                if brand and branch:
                    print (json.dumps(res_dic, ensure_ascii=False).encode('utf8'))
                else:
                    sys.stderr.write('{}\n'.format(json.dumps(res_dic, ensure_ascii=False).encode('utf8')))


def bracket_com_name():
    for line in sys.stdin:
        ln = line.strip()
        res_dic = parse_shop_name(ln)
        bracket_ls = res_dic['bracket']
        remain_ls = res_dic['remain']
        len_b = len(bracket_ls)
        for b_cont in bracket_ls:
            print (b_cont.strip().encode('utf8'))
#            if not b_cont.endswith(u'店'):
#                print (ln)


def filter_chars(ss):
    '''
    过滤得到不关心的字符
    :param ss: 输入字符
    :return: 不关心字符
    '''
    if isinstance(ss, str):
        ss = ss.decode('utf8')
    char_filter = re.compile(u'[\u4E00-\u9FA5A-Za-z0-9\(\)（）]') # 过滤出中文 字母 数字 其余符号用空格表示
    ss1 = char_filter.sub('', ss)
    return ss1

def get_all_filtered_chars():
    for line in sys.stdin:
        ln = line.strip()
        res_char = filter_chars(ln)
        if res_char:
            print (res_char.encode('utf8'))

def test_parse_shop_name():
    ss = u'陈奕迅演唱((十年))、（浮夸）、(不要说话)'
    res_dic = parse_shop_name(ss)
    print (json.dumps(res_dic, ensure_ascii=False).encode('utf8'))

def test_filter_chars():
    ss = u'陈奕迅演唱(十年)、（浮夸）、(不要说话)'
    filtered_str = filter_chars(ss)
    print (filtered_str)

if __name__ == '__main__':
    sn_norm_obj = ShopNameNormalizer()
    #sn_norm_obj.parse_branch_from_file('meb_shop_name_no_dup.txt')
    #sn_norm_obj.parse_brand_from_file('meb_shop_name_no_dup.txt')
    sn_norm_obj.parse_brand_and_branch_from_file('meb_shop_name_no_dup.txt')
    #sn_norm_obj.parse_shop_name_from_file('meb_shop_name_no_dup.txt')
    #filter_cand_remain()
    #get_all_cand_branch_with_spec_suffix()
    #get_all_filtered_chars()
    #test_filter_chars()
    #test_parse_shop_name()
    #bracket_com_name()
