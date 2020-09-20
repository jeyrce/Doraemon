# coding=utf-8
"""
__purpose__ = 自定义表单
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 20:42]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""

from django.contrib.auth.forms import PasswordResetForm

from Task.mail import send_password_rest_link


class AsyncMailPasswordResetForm(PasswordResetForm):
    """
    覆盖父类同步发送邮件,此处使用异步任务
    """

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None
    ):
        send_password_rest_link.delay(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None
        )
