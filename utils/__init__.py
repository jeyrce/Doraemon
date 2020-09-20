# coding=utf-8
"""
__purpose__ = 常用工具类
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 17:51]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import logging

from Doraemon.model import System

logger = logging.getLogger(__name__)


def get_from_db(key, type_, default=None):
    """
    key: 获取的键
    type_: 预期的值类型, 也可以是一个可执行对象
    default: 获取不到值时的默认值
    """
    item = System.objects.filter(key=key).first()
    if not item:
        return default
    assert callable(type_), f"Not supported type: {type_}"
    try:
        return type_(item.value)
    except Exception as e:
        logger.exception(e)
    return default
