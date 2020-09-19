# coding=utf-8
"""
__purpose__ = 后台管理系统
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 18:34]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model

from Doraemon.model import *

UserProfile = get_user_model()

admin.site.site_header = 'xoo.site'
admin.site.site_title = 'Doraemon'


class CommonAdmin(admin.ModelAdmin):
    """
    公共的设置
    """
    list_select_related = False
    list_per_page = 100
    list_max_show_all = 200
    date_hierarchy = None
    save_as = False
    save_as_continue = True
    save_on_top = False
    preserve_filters = True


class UserAdmin(CommonAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "is_superuser")
    list_display_links = ()
    list_filter = ("is_superuser", "is_staff", "is_active")
    list_editable = ("is_superuser", "is_staff", "is_active")
    search_fields = ("username", "email")
    inlines = []


class RobotAdmin(CommonAdmin):
    list_display = ("name", "is_active", "group", "mode", "by")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("name", "is_active", "mode")
    search_fields = ("name", "group")
    inlines = []


class MessageAdmin(CommonAdmin):
    list_display = ("task", "is_active", "robot__name", "by")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("task", "robot__name")
    inlines = []


class KeywordAdmin(CommonAdmin):
    list_display = ("word", "is_active", "by", "create")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("is_active", "word")
    search_fields = ("word",)
    inlines = []


class LinkAdmin(CommonAdmin):
    list_display = ("title", "keywords", "by")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("title", "is_active")
    search_fields = ("title", "keywords__name")
    inlines = []


class ClickAdmin(CommonAdmin):
    list_display = ("ip", "create")
    list_display_links = ()
    list_filter = ()
    list_editable = ()
    search_fields = ("ip",)
    inlines = []


class SearchAdmin(ClickAdmin):
    pass


class AttendanceAdmin(CommonAdmin):
    list_display = ("date", "worker__name", "is_active", "active")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ()
    search_fields = ("data",)
    inlines = []


class SystemAdmin(CommonAdmin):
    list_display = ("key", "value", "is_active", "remark", "by")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("value", "is_active", "remark")
    search_fields = ("key", "remark")
    inlines = []


admin.register(UserProfile, UserAdmin)
admin.register(Robot, RobotAdmin)
admin.register(Message, MessageAdmin)
admin.register(Keyword, KeywordAdmin)
admin.register(Link, LinkAdmin)
admin.register(Click, ClickAdmin)
admin.register(Search, SearchAdmin)
admin.register(Attendance, AttendanceAdmin)
admin.register(System, SystemAdmin)
