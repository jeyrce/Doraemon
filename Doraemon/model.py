# coding=utf-8
"""
__purpose__ = 机器人数据表模型
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/15 16:51]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import time
import uuid
import json
import random

import requests
from django.contrib.auth import get_user_model
from django.db.models import *
from django.db.models.fields import *
from django.template import Template, Context

from Doraemon.settings import GOTO_URL, TASKS

UserProfile = get_user_model()

__all__ = [
    "Robot", "Message", "Keyword", "Link", "Click", "Search", "Attendance", "System",
]


class Robot(Model):
    """
    机器人
    """
    MODES = (
        ("wechat", "企业微信"),
        ("dingtalk", "钉钉"),
        ("other", "其他类型"),
    )
    name = CharField(max_length=32, null=False, blank=False, unique=True, verbose_name="机器人名称")
    group = CharField(max_length=64, null=False, blank=False, verbose_name="群组名称")
    api = URLField(unique=True, null=False, blank=False, verbose_name="机器人链接地址")
    mode = CharField(choices=MODES, max_length=16, null=False, blank=False, verbose_name="类型")
    create = DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update = DateTimeField(auto_now=True, verbose_name="上次修改")
    # 需要在admin_model中重写save方法来获取当前登录对象, 删除用户对象时置空
    by = ForeignKey(UserProfile, on_delete=SET_NULL, null=True, verbose_name="创建人")
    is_active = BooleanField(default=True, null=False, blank=False, verbose_name="是否可用")
    remark = CharField(max_length=64, blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name_plural = verbose_name = "机器人"
        db_table = "robot"

    def __str__(self):
        return f"[{self.group}]{self.name}"


class Message(Model):
    """
    需要定时推送的消息主题
    """
    task = CharField(max_length=32, unique=True, null=False, blank=False, verbose_name="任务名称", choices=TASKS)
    content = TextField(null=True, blank=True, verbose_name="消息内容")
    robot = ForeignKey(Robot, on_delete=SET_NULL, null=True, verbose_name="推送机器人", limit_choices_to={"is_active": True})
    create = DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update = DateTimeField(auto_now=True, verbose_name="上次修改")
    # 需要在admin_model中重写save方法来获取当前登录对象, 删除用户对象时置空
    by = ForeignKey(UserProfile, on_delete=SET_NULL, null=True, verbose_name="创建人")
    is_active = BooleanField(default=True, null=False, blank=False, verbose_name="是否可用")
    remark = CharField(max_length=64, blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name_plural = verbose_name = "消息"
        db_table = "message"

    def __str__(self):
        return self.task

    def send(self, duty, duty_list):
        """
        消息推送给机器人平台
        """
        time.sleep(random.random() * 10)  # 随机 0-10s分布，避免同一时刻大量推送
        send_func = getattr(self, f"_send_to_{self.robot.mode}", "xxx")
        if callable(send_func):
            return send_func(duty, duty_list)

    def _send_to_wechat(self, duty, duty_list):
        """
        消息推送给微信平台
        """
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "text",
            "text": {
                "mentioned_list": ["@all", ],
                "content": Template(self.content).render(
                    Context({
                        "duty": duty,  # 今日值班
                        "duty_list": duty_list,  # 最近七天的值班
                    })
                ),
            }
        }
        try:
            response = requests.post(self.robot.api, json=data, headers=headers, timeout=20)
            result = response.json()
        except Exception as e:
            return False, e
        else:
            if result.get("errcode", 1) == 0:
                return True, json.dumps(result)
            return False, json.dumps(result)

    def _send_to_dingtalk(self, duty, duty_list):
        """
        TODO: 消息推送给钉钉
        """
        return False, f"Not supported robot type [{self.robot.mode}]."

    def _send_to_other(self, duty, duty_list):
        """
        TODO: 更多类型的机器人支持
        """
        return False, f"Not supported robot type [{self.robot.mode}]."


class Keyword(Model):
    """
    群消息关键字
    """
    word = CharField(max_length=16, blank=False, null=False, verbose_name="关键字")
    create = DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update = DateTimeField(auto_now=True, verbose_name="上次修改")
    # 需要在admin_model中重写save方法来获取当前登录对象, 删除用户对象时置空
    by = ForeignKey(UserProfile, on_delete=SET_NULL, null=True, verbose_name="创建人")
    is_active = BooleanField(default=True, null=False, blank=False, verbose_name="是否可用")
    remark = CharField(max_length=64, blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name_plural = verbose_name = "关键字"
        db_table = "keyword"

    def __str__(self):
        return self.word

    def searched(self):
        """
        关键字下的搜索次数
        """
        return Search.objects.filter(keyword_id=self.id).count()

    searched.short_description = "搜索次数"


class Link(Model):
    """
    常用连接表
    """
    title = CharField(max_length=64, blank=False, null=False, verbose_name="连接标题")
    keywords = ManyToManyField(Keyword, related_name="keywords_set",
                               limit_choices_to={"is_active": True}, verbose_name="关键字")
    link = URLField(unique=True, blank=False, null=False, verbose_name="链接地址")
    create = DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update = DateTimeField(auto_now=True, verbose_name="上次修改")
    # 需要在admin_model中重写save方法来获取当前登录对象, 删除用户对象时置空
    by = ForeignKey(UserProfile, on_delete=SET_NULL, null=True, verbose_name="创建人")
    is_active = BooleanField(default=True, null=False, blank=False, verbose_name="是否可用")
    remark = CharField(max_length=64, blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name_plural = verbose_name = "链接"
        db_table = "link"

    def __str__(self):
        return self.title

    def goto_url(self):
        """通过本站跳转的url"""
        return f"/{GOTO_URL}?link={self.link}"

    goto_url.short_description = "跳转链接"

    def clicked(self):
        """点击次数统计"""
        return Click.objects.filter(link_id=self.id).count()

    clicked.short_description = "点击次数"


class Click(Model):
    """
    统计链接点击次数
    """
    link = ForeignKey(Link, on_delete=PROTECT, null=False, blank=False, verbose_name="对应链接")
    create = DateTimeField(auto_now_add=True, verbose_name="添加时间")
    ip = GenericIPAddressField(null=True, blank=True, verbose_name="点击来源")
    device = CharField(max_length=200, blank=True, null=True, verbose_name="设备类型")

    class Meta:
        verbose_name_plural = verbose_name = "点击记录"
        db_table = "click"

    def __str__(self):
        return self.ip


class Search(Model):
    """
    搜索记录统计
    """
    keyword = ForeignKey(Keyword, on_delete=PROTECT, null=False, blank=False, verbose_name="关键字")
    create = DateTimeField(auto_now_add=True, verbose_name="添加时间")
    ip = GenericIPAddressField(null=True, blank=True, verbose_name="点击来源")
    device = CharField(max_length=200, blank=True, null=True, verbose_name="设备类型")

    class Meta:
        verbose_name_plural = verbose_name = "搜索记录"
        db_table = "search"

    def __str__(self):
        return self.ip


class Attendance(Model):
    """
    排班表: 根据system表值班组id列表每几天创建
    """
    date = DateField(unique=True, null=False, blank=False, verbose_name="值班日期",
                     error_messages={'unique': '当天已存在值班人，请先移除或修改记录'})
    worker = ForeignKey(UserProfile, related_name="days", null=False, blank=False, on_delete=PROTECT,
                        verbose_name="责任人")
    token = UUIDField(unique_for_year=True, blank=True, null=False, verbose_name="签到Token", default=uuid.uuid4().hex)
    create = DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name="添加时间")
    by = ForeignKey(UserProfile, related_name="creates", null=False, blank=False, on_delete=PROTECT, verbose_name="创建人")
    active = DateTimeField(null=True, blank=True, verbose_name="签到时间", help_text="为空则表示未签到")
    ip = GenericIPAddressField(null=True, blank=True, verbose_name="点击来源")
    device = CharField(max_length=200, blank=True, null=True, verbose_name="设备类型")

    class Meta:
        verbose_name_plural = verbose_name = "排班"
        db_table = "attendance"

    def __str__(self):
        return self.date.strftime("%Y/%m/%d")

    def is_active(self):
        """
        是否已完成签到
        """
        return "Yes" if self.active else "No"

    is_active.short_description = "是否已签到"

    def weekday(self):
        """
        返回星期中的位置
        """
        day_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return day_map[self.date.weekday()]

    weekday.short_description = "工作日"

    def worker_name(self):
        return f"{self.worker.last_name}{self.worker.first_name}"

    worker_name.short_description = "姓名"


class System(Model):
    """
    系统配置: 在项目初始化的时候插入记录，平时仅允许修改，不允许增加或删除
    """
    key = CharField(max_length=32, null=False, blank=False, unique=True, verbose_name="键")
    value = TextField(max_length=128, null=False, blank=False, verbose_name="值", help_text="最长128字符")
    create = DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update = DateTimeField(auto_now=True, verbose_name="上次修改")
    # 需要在admin_model中重写save方法来获取当前登录对象, 删除用户对象时置空
    by = ForeignKey(UserProfile, on_delete=SET_NULL, null=True, verbose_name="创建人")
    remark = CharField(max_length=64, blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name_plural = verbose_name = "系统配置"
        db_table = "system"

    def __str__(self):
        return self.remark
