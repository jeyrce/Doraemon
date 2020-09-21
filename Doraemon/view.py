# coding=utf-8
"""
__purpose__ = 业务逻辑
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/15 20:50]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import datetime

from django.views.generic import RedirectView, View, TemplateView, ListView
from django.http.response import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView

from Doraemon.forms import AsyncMailPasswordResetForm
from Doraemon.model import Link, Attendance, Search, Click
from utils import get_from_db

__all__ = [
    "IndexView", "GoToView", "SearchView", "SignView", "PasswordResetView", "AsyncMailPasswordResetView", "alive_view",
]


class IndexView(ListView):
    """
    首页显示最近一周的排班情况
    TODO: 展示高频搜索关键字词云，链接点击次数统计等
    """

    ordering = "date"
    template_name = "index.html"

    def get_queryset(self):
        return Attendance.objects.filter(
            date__gte=datetime.date.today(),
            date__lte=datetime.date.today() + datetime.timedelta(days=get_from_db('SHOW_DUTY_DAYS', int, 7)),
        )


class GoToView(View):

    def get(self, request):
        link = Link.objects.filter(link=request.GET.get("link", "")).first()
        if not link:
            raise Http404
        Click.objects.create(link_id=link.id, ip=request.CLIENT["ip"], device=request.CLIENT["device"])
        return redirect(link.link)


class SearchView(View):

    def get(self, request):
        # TODO: 搜索记录表插入记录
        return JsonResponse({"code": 0, "message": "ok", "data": None})


class SignView(View):
    """
    值班签到
    """

    def get(self, request):
        # 更新签到表，返回成功结果
        today_attendance = Attendance.objects.filter(date=datetime.date.today()).first()
        attendance = Attendance.objects.filter(token=request.GET.get("token")).first()
        data = {
            "date": today_attendance.date,
            "weekday": today_attendance.weekday(),
            "username": today_attendance.worker.get_full_name(),
            "succeed": True,
            "message": "请关注问题群消息，回应项目问题并及时更新问题进展！"
        }
        if (not attendance) or (attendance.date != datetime.date.today()):
            data["succeed"] = False
            data["message"] = "无效token!"
        elif attendance.is_active():
            data["succeed"] = False
            data["message"] = "已经签到完成，无需再次点击！"

        return render(request, "message/sign.html", data)


class AsyncMailPasswordResetView(PasswordResetView):
    """
    cover原有逻辑, 采用异步任务发送邮件
    """
    form_class = AsyncMailPasswordResetForm


async def alive_view(request):
    """
    返回系统正常的结果
    """
    import time
    time.sleep(12)
    return JsonResponse({"code": 0, "data": request.CLIENT, "message": "OK"})
