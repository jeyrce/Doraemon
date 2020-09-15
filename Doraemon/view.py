# coding=utf-8
"""
__purpose__ = 业务逻辑
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/15 20:50]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

from django.views.generic import RedirectView

from Doraemon.model import Link

__all__ = [
    "GoToView",
]


class GoToView(RedirectView):
    permanent = False
    url = None
    pattern_name = "文档链接"
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        link = Link.objects.filter(link=kwargs.get("link", None)).first()
        if not link:
            return "404.html"
        # 统计链接点击次数
        link.click += 1
        link.save()
        return link.goto_url()
