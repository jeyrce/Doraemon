# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 16:01]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import celery

app = celery.Celery("Doraemon")

app.config_from_object("Task.settings")

app.autodiscover_tasks([
    "Task.mail",
    "Task.message",
])
