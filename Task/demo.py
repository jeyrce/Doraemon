# coding=utf-8
"""
__purpose__ = Task demo for celery async function
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/22 12:34]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

from utils import db_flush

from Task import app


@db_flush
@app.task
def demo(*args):
    pass
