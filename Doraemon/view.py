# coding=utf-8
"""
__purpose__ = 业务逻辑
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/15 20:50]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import datetime

from django.views.generic import RedirectView, View, TemplateView, ListView
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView

from Doraemon.forms import SyncMailPasswordResetForm
from Doraemon.model import Link, Attendance
from utils import get_from_db

__all__ = [
    "IndexView", "GoToView", "SearchView", "SignView", "PasswordResetView", "SyncMailPasswordResetView",
]


class IndexView(ListView):
    """
    首页显示最近一周的排班情况
    TODO: 展示高频搜索关键字词云，链接点击次数统计等
    """

    ordering = "date"
    template_name = "index.html"
    queryset = Attendance.objects.filter(
        date__gte=datetime.date.today(),
        date__lte=datetime.date.today() + datetime.timedelta(days=get_from_db("SHOW_DUTY_DAYS", int, 7)),
    )


class GoToView(View):

    def get(self, request):
        # TODO: 点击表插入记录
        return JsonResponse({"code": 0, "message": "ok", "data": None})


class SearchView(View):

    def get(self, request):
        # TODO: 搜索记录表插入记录
        return JsonResponse({"code": 0, "message": "ok", "data": None})


class SignView(View):
    """
    值班签到
    """

    def get(self, request):
        # TODO: 值班人打开连接后标记已签到
        return render(request, "message/sign.html", {"succeed": True})


class SyncMailPasswordResetView(PasswordResetView):
    """
    cover原有逻辑, 采用异步任务发送邮件
    """
    form_class = SyncMailPasswordResetForm
