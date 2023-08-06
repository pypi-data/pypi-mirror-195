#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "ITXiaoPang"
__mtime__ = "2020/07/29"
__project__ = "split-mysql"
__IDE__ = "PyCharm"

__version__ = '1.00.01'

import ctypes
import json
import os
import platform


go_func_split_mysql = ctypes.CDLL(
    f'{os.path.abspath(os.path.dirname(__file__))}/_parser4mysql_{platform.system()}.so'
).splitMySQL
go_func_split_mysql.argtypes = [ctypes.c_char_p]
go_func_split_mysql.restype = ctypes.c_char_p


def split_mysql(statement: str):
    ret_go_func = ''
    try:
        statement_encode = statement.encode('utf-8')
        go_func_split_mysql_ret = go_func_split_mysql(statement_encode)

        try:
            ret_go_func = go_func_split_mysql_ret.decode('utf-8')
        except UnicodeDecodeError:
            ret_go_func = go_func_split_mysql_ret.decode('unicode_escape')

        ret_list_go_func = json.loads(ret_go_func)
        ret = []
        for each_statement in ret_list_go_func:
            # 去空行
            each_statement_list = [x for x in str(each_statement).split('\n') if x.strip()]
            ret.append('\n'.join(each_statement_list))
    except json.JSONDecodeError:
        ret = f'语句拆解失败:{ret_go_func}。'
    except Exception as ex:
        ret = f'语句拆解异常：{str(ex)}。'
    return ret
