# coding=utf-8
"""
__purpose__ = Message tasks
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 16:06]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import logging

from Task import app

logger = logging.getLogger(__name__)


@app.task
def notice_on_time(*args):
    """
    从消息表筛选出结果进行推送到机器人
    """
    pass
