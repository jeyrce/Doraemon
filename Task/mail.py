# coding=utf-8
"""
__purpose__ = Mail tasks
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 16:05]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import logging

from Task import app

logger = logging.getLogger(__name__)


@app.task
def yesterday_count(*args):
    """
    TODO: 汇总上一天搜索和点击记录邮件推送给项目经理
    """
    pass
