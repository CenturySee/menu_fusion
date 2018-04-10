#/bin/python
#coding=utf8

import os
import sys
import random

def random_sample(num = 100):
    all_ls = []
    for line in sys.stdin:
        ln = line.strip()
        if ln:
            all_ls.append(ln)
    res_ls = []
    if len(all_ls) > num:
        res_ls = random.sample(all_ls, num)
    else:
        res_ls = all_ls
    res_ls = sorted(res_ls)
    print ('\n'.join(res_ls))

if __name__ == '__main__':
    try:
        num = int(sys.argv[1])
    except:
        num = 100
    random_sample(num)

