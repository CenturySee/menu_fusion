#!/usr/bin/python
# coding=utf8

import os
import sys
import json
import zlib
import base64
import traceback

from collections import OrderedDict

#from WebSpider.util import jsonCompress, jsonDecompress

def jsonCompress(content):
    return base64.encodestring(zlib.compress(json.dumps(content)))

def jsonDecompress(content):
    try:
        return json.loads(zlib.decompress(base64.decodestring(content)))
    except:
        return content

cur_dir = os.path.dirname(os.path.abspath(__file__))
proj_dir = os.sep.join([cur_dir, '..'])
conf_dir = os.sep.join([proj_dir, 'conf'])
utils_dir = os.sep.join([proj_dir, 'utils'])

sys.path.append(utils_dir)
from mysql_operation import get_mysql_obj
