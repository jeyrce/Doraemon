# coding=utf-8
"""
__purpose__ = 权限、认证
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 20:53]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from utils import get_from_db

UserAccount = get_user_model()


class EmailUsernameAuthBackend(ModelBackend):
    """
    使用email或者用户名作为账户登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            account = UserAccount.objects.get(Q(email=username) | Q(username=username))
        except UserAccount.DoesNotExist:
            pass
        else:
            if account.check_password(password) and self.user_can_authenticate(account):
                if get_from_db("UPGRADING", int, 0):
                    if not account.is_superuser:
                        # 维护期间不允许超管之外的人登录
                        account.is_staff = False
                return account


class QQAuthBackend(ModelBackend):
    """
    TODO: 使用qq第三方登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        pass


class GithubAuthBackend(ModelBackend):
    """
    TODO: 使用github第三方登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        pass


class WechatAuthBackend(ModelBackend):
    """
    TODO: 使用微信第三方登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        pass
