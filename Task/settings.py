# coding=utf-8
"""
__purpose__ = Settings for celery worker.
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 16:03]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import os
import datetime

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Doraemon.settings")
django.setup()
from kombu import Exchange, Queue
from celery.schedules import crontab
from celery import platforms

from Doraemon.settings import TASKS, REDIS_AUTH

platforms.C_FORCE_ROOT = True  # 允许root用户启动worker

# 记录日志
CELERYD_HIJACK_ROOT_LOGGER = True
CELERY_TIMEZONE = 'Asia/Shanghai'

# 注册Celery任务, 或者使用celery.autodiscover_tasks也可
CELERY_IMPORTS = (
    "Task.mail",
    "Task.message",
    "Task.demo",
)

# 序列化方法
CELERY_TASK_SERIALIZER = "pickle"
# 指定任务接受的序列化类型.
CELERY_ACCEPT_CONTENT = ["msgpack", "pickle", "json", "yaml", ]
# 结果序列化方法
CELERY_RESULT_SERIALIZER = "pickle"
# 结果保存
CELERY_RESULT_BACKEND = 'redis://:{password}@{ip}:{port}/7'.format(**REDIS_AUTH)
# Broker使用redis
BROKER_URL = 'redis://:{password}@{ip}:{port}/8'.format(**REDIS_AUTH)

default_exchange = Exchange('default', type='direct')
topic_exchange = Exchange('topic', type='topic')
fanout_exchange = Exchange('fanout', type='fanout')

CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('topic', topic_exchange, routing_key='topic'),
    Queue('fanout', fanout_exchange, routing_key='fanout'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'

# 定时任务配置如下
CELERYBEAT_SCHEDULE = {
    # 定时query任务保持mysql连接
    TASKS[5][1]: {
        "task": "Task.message.alive_send",
        "schedule": datetime.timedelta(hours=1),
        "args": TASKS[5],
    },
    # 值班群定时提醒任务
    TASKS[0][1]: {
        'task': 'Task.message.notice_on_time',
        'schedule': crontab(hour='09', minute='00'),
        'args': TASKS[0],
    },
    TASKS[1][1]: {
        'task': 'Task.message.notice_on_time',
        'schedule': crontab(hour='18', minute='00'),
        'args': TASKS[1],
    },
    # 问题群定时提醒任务
    TASKS[2][1]: {
        'task': 'Task.message.notice_on_time',
        'schedule': crontab(hour='09', minute='00'),
        'args': TASKS[2],
    },
    TASKS[3][1]: {
        'task': 'Task.message.notice_on_time',
        'schedule': crontab(hour='14', minute='00'),
        'args': TASKS[3],
    },
    TASKS[4][1]: {
        'task': 'Task.message.notice_on_time',
        'schedule': crontab(hour='18', minute='00'),
        'args': TASKS[4],
    },
    # 系统提醒
    '昨日搜索和点击统计': {
        'task': 'Task.mail.yesterday_count',
        'schedule': crontab(hour='09', minute='30'),
        'args': (),
    },
    "每日更新值班表": {
        "task": "Task.message.update_attendance",
        "schedule": crontab(hour="03", minute="00"),
        "args": (),
    },
    # 研发群每日提醒
    TASKS[6][1]: {
        "task": "Task.message.notice_on_time",
        "schedule": crontab(hour="09", minute="00"),
        "args": TASKS[6],
    },
    # 管理节点巡检提醒
    TASKS[7][1]: {
        "task": "Task.message.notice_on_time",
        "schedule": crontab(day_of_week="friday", hour="14", minute="50"),
        "args": TASKS[7],
    },
    # 镜像仓库运维提醒
    TASKS[8][1]: {
        "task": "Task.message.notice_on_time",
        "schedule": crontab(day_of_week="friday", hour="17", minute="00"),
        "args": TASKS[8],
    },
    # 小团队技术分享提醒
    TASKS[9][1]: {
        "task": "Task.message.notice_on_time",
        "schedule": crontab(day_of_week="thursday", hour="09", minute="30"),
        "args": TASKS[9],
    },
}
