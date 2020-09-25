# coding=utf-8
"""
__purpose__ = Message tasks
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 16:06]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import datetime
import logging

from django.contrib.auth import get_user_model

from Task import app
from Doraemon.model import Message, Attendance
from utils import get_from_db, get_next_username, get_default_duty_and_list

UserProfile = get_user_model()
logger = logging.getLogger(__name__)


@app.task
def notice_on_time(*args):
    """
    从消息表筛选出结果进行推送到机器人
    """
    code, title = args
    logger.info(f"[{title}]start push message...")
    message = Message.objects.filter(task=code).first()
    if message and message.is_active:
        duty, list_ = get_default_duty_and_list()
        _, msg = message.send(duty, list_)
        logger.info(f"[{title}push message over: {msg}")


@app.task
def update_attendance(*args):
    """
    每天检查排班表，如果数量不足7天, 则创建接下来一天的排班记录
    以此达到效果： 总是能看到从当前时间往后推一周的排班计划
    """
    logger.info("start update attendance...")
    today = datetime.date.today()
    attendances = Attendance.objects.filter(date__gte=today).order_by("date")
    last = attendances.last()
    if attendances.count() < get_from_db("SHOW_DUTY_DAYS", int, 7):
        next_username = get_next_username(last.username)
        if next_username:
            next = {
                "date": last.date + datetime.timedelta(days=1),
                "worker": UserProfile.objects.filter(username=next_username),
            }
            try:
                Attendance.objects.create(**next)
            except Exception as e:
                logger.exception(e)
            else:
                logger.info("update attendance succeed...")
            return
        logger.error("got next_username failed...")
    logger.info("attendance's update not needed...")


@app.task
def alive_send(*args):
    """
    - 每小时提醒任务存活
    - 每小时执行一次MySQL查询，让连接保持状态
    """
    code, title = args
    logger.info(f"Start push alive message...")
    message = Message.objects.filter(task=code).first()
    if message and message.is_active:
        duty, list_ = get_default_duty_and_list()
        _, result = message.send(duty, list_)
        logger.info(f"Push alive status over: {result}")
