# coding=utf-8
"""
__purpose__ = 项目部署时的初始化操作
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 21:00]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Doraemon.settings")
django.setup()

from Doraemon.model import System

KEYS = [
    {"key": "SHOW_DUTY_DAYS", "value": "7", "remark": "首页显示的值班天数"},
    {"key": "UPGRADING", "value": "0", "remark": "网站是否处于维护状态"},
]

if __name__ == '__main__':
    # 初始化数据库表
    for key in KEYS:
        System.objects.create(**key)
