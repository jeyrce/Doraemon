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

from Doraemon.settings import TASKS, KEYS
from Doraemon.model import *

if __name__ == '__main__':
    print("初始化日志文件夹")
    log_dir = "/var/log/Doraemon"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    print("初始化系统配置")
    for key in KEYS:
        item = System.objects.filter(key=key["key"])
        if item.count() > 0:
            print(f">{key['remark']} SKIPPED")
            continue
        System.objects.create(**key)
        print(f">{key['remark']} SUCCEED")

    print("初始化推送消息")
    for task in TASKS:
        message = Message.objects.filter(task=task[0])
        if message.count() > 0:
            print(f">{task[1]} SKIPPED")
            continue
        Message.objects.create(task=task[0], remark=task[1])
        print(f">{task[1]} SUCCEED")

    print("所有初始化操作结束")
