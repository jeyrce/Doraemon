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

admin.site.site_header = 'Doraemon'
admin.site.site_title = '系统管理'

Account = get_user_model()


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

    # LOOK: 目前增删改只能超管权限，否则仅拥有查看权限
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return True
        return False


class RecordAdmin(CommonAdmin):
    """
    中间件统计的记录不允许后台变更
    """

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ByUserMixin(object):

    def save_model(self, request, obj, form, change):
        # 获取当前创建人
        obj.by = request.user
        obj.save()


class UserAdmin(CommonAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "is_superuser")
    list_display_links = ()
    list_filter = ("is_superuser", "is_staff", "is_active")
    list_editable = ("is_superuser", "is_staff", "is_active")
    search_fields = ("username", "email")
    inlines = []
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login',)
    exclude = ("password",)
    style_fields = {'user_permissions': 'm2m_transfer'}
    fieldsets = (
        ("基本信息", {"fields": ("email", "username", 'last_name', 'first_name',)}),
        ("账户状态", {"fields": ("is_active", "is_staff", "is_superuser",)}),
        ("权限信息", {"fields": ('groups', 'user_permissions')}),
        ("统计信息", {"fields": ("date_joined", "last_login",)}),
    )


class RobotAdmin(ByUserMixin, CommonAdmin):
    list_display = ("name", "is_active", "group", "mode", "by")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("is_active", "mode")
    search_fields = ("name", "group")
    inlines = []
    ordering = ('-create',)
    readonly_fields = ('create', 'update', "by",)
    fieldsets = (
        ("基本信息", {"fields": ("api", 'mode', "name", "group", 'is_active', "remark",)}),
        ("其他信息", {"fields": ("by", "create", "update",)}),
    )


class MessageAdmin(ByUserMixin, CommonAdmin):
    list_display = ("task", "is_active", "robot", "by")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("task",)
    inlines = []
    ordering = ('-create',)
    readonly_fields = ('create', 'update', "by")
    fieldsets = (
        ("基本信息", {"fields": ("task", 'robot', "is_active", "content", "remark",)}),
        ("其他信息", {"fields": ("by", "create", "update",)}),
    )


class KeywordAdmin(ByUserMixin, CommonAdmin):
    list_display = ("word", "is_active", "by", "searched")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("word",)
    inlines = []
    ordering = ('-create',)
    readonly_fields = ('by', 'create', "update", "searched")
    exclude = ()
    fieldsets = (
        ("词条信息", {"fields": ("word", "is_active", "remark",)}),
        ("其他信息", {"fields": ("searched", "by", "create", "update",)}),
    )


class LinkAdmin(ByUserMixin, CommonAdmin):
    list_display = ("title", "is_active", "by", "clicked")
    list_display_links = ()
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("title",)
    inlines = []
    ordering = ('-create',)
    readonly_fields = ('by', 'create', "update", "clicked")
    style_fields = {'keywords': 'm2m_transfer'}
    fieldsets = (
        ("基本信息", {"fields": ("title", "link", "is_active", 'keywords', "remark",)}),
        ("其他信息", {"fields": ("clicked", "by", "create", "update",)}),
    )


class ClickAdmin(RecordAdmin):
    list_display = ("ip", "create")
    list_display_links = ()
    list_filter = ()
    list_editable = ()
    search_fields = ("ip",)
    inlines = []
    ordering = ('-create',)
    readonly_fields = ('ip', 'link', "create", "device")


class SearchAdmin(ClickAdmin):
    readonly_fields = ('ip', 'keyword', "create", "device")


class AttendanceAdmin(ByUserMixin, CommonAdmin):
    list_display = ("date", "worker", "is_active", "active")
    list_display_links = ()
    list_filter = ()
    list_editable = ()
    search_fields = ("date",)
    inlines = []
    ordering = ('-date',)
    readonly_fields = ('token', 'create', "by", "active", "ip", "device", "is_active")
    fieldsets = (
        ("值班信息", {"fields": ("date", "worker", 'token',)}),
        ("签到信息", {"fields": ("is_active", "active", "ip", "device",)}),
        ("其他信息", {"fields": ("by", 'create',)}),
    )


class SystemAdmin(ByUserMixin, CommonAdmin):
    list_display = ("key", "value", "remark", "by")
    list_display_links = ()
    list_editable = ("value", "remark")
    search_fields = ("key", "remark")
    inlines = []
    ordering = ('-create',)
    readonly_fields = ('create', 'update', "by", "key")
    fieldsets = (
        ("主要信息", {"fields": ("key", "value", 'remark',)}),
        ("其他信息", {"fields": ("by", "create", "update",)}),
    )

    # 仅允许初始化部署时写入，平时不允许删除或增加，只能修改

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.unregister(Account)  # 首先取消系统的自动注册
admin.site.register(Account, UserAdmin)
admin.site.register(Robot, RobotAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Click, ClickAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(System, SystemAdmin)
