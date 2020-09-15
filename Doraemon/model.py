# coding=utf-8
"""
__purpose__ = 机器人数据表模型
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/15 16:51]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""
from django.contrib.auth import get_user_model
from django.db.models import *
from django.db.models.fields import *

from Doraemon.settings import GOTO_URL

UserProfile = get_user_model()


class ModelMixin(object):
    """数据模型公共属性"""
    create = DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update = DateTimeField(auto_now=True, verbose_name="上次修改")
    # 需要在admin_model中重写save方法来获取当前登录对象, 删除用户对象时置空
    by = ForeignKey(UserProfile, on_delete=SET_NULL, null=True, verbose_name="创建人")
    is_active = BooleanField(default=True, null=False, blank=False, verbose_name="是否可用")
    remake = CharField(max_length=64, blank=True, null=True, verbose_name="备注")


class Robot(Model, ModelMixin):
    """
    机器人
    """
    MODES = (
        ("A", "企业微信"),
        ("B", "钉钉"),
        ("C", "其他类型"),
    )
    name = CharField(max_length=32, null=False, blank=False, unique=True, verbose_name="机器人名称")
    group = CharField(max_length=64, null=False, blank=False, verbose_name="群组名称")
    api = URLField(unique=True, null=False, blank=False, verbose_name="机器人链接地址")
    mode = CharField(choices=MODES, max_length=1, null=False, blank=False, verbose_name="类型")

    class Meta:
        verbose_name_plural = verbose_name = "机器人表"
        db_table = "robot"

    def __str__(self):
        return f"[{self.group}]{self.name}"


class Keyword(Model, ModelMixin):
    """
    群消息关键字
    """
    word = CharField(blank=False, null=False, verbose_name="关键字")
    search = PositiveIntegerField(default=0, null=False, blank=False, verbose_name="搜索次数")

    class Meta:
        verbose_name_plural = verbose_name = "关键字表"
        db_table = "keyword"

    def __str__(self):
        return self.word

    def click(self):
        """
        关键字下的链接搜索次数
        """
        return self.keywords_set.count()


class Link(Model, ModelMixin):
    """
    常用连接表
    """
    title = CharField(max_length=64, blank=False, null=False, verbose_name="连接标题")
    keywords = ManyToManyField(Keyword, related_name="keywords_set",
                               limit_choices_to={"is_active": True}, verbose_name="关键字")
    link = URLField(blank=False, null=False, verbose_name="链接地址")
    click = PositiveIntegerField(blank=False, null=False, default=0, verbose_name="链接点击次数")

    class Meta:
        verbose_name_plural = verbose_name = "链接表"
        db_table = "link"

    def __str__(self):
        return self.title

    def goto_url(self):
        """通过本站跳转的url"""
        return f"{GOTO_URL}?link={self.link}"
