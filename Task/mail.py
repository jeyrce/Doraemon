# coding=utf-8
"""
__purpose__ = Mail tasks
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/19 16:05]
    
    Copyright (c) 2020 JeeysheLu
    
This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import logging

from django.template import loader
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMultiAlternatives

from Task import app
from Doraemon.settings import EMAIL_SUBJECT_PREFIX, SERVER_EMAIL
from utils import db_flush

logger = logging.getLogger(__name__)

add_prefix = lambda txt: '{}{}'.format(EMAIL_SUBJECT_PREFIX, txt) if not txt.startswith(EMAIL_SUBJECT_PREFIX) else txt


@db_flush
@app.task()
def yesterday_count(*args):
    """
    TODO: 汇总上一天搜索和点击记录邮件推送给项目经理
    """
    pass


@db_flush
@app.task()
def send_one(subject, message, recipient_list, html=None):
    """
    发送一条消息: 自动添加主题前缀和签名
    """
    send_mail(
        subject=add_prefix(subject),
        message=message,
        from_email=SERVER_EMAIL,
        recipient_list=recipient_list,
        html_message=html,
    )


@db_flush
@app.task()
def send_many_text(data_tuple):
    """
    一次性发送多条消息: 自动添加前缀和主题签名
    datatuple:
    (
        (subject0, message0, sender, recipient),
        (subject1, message1, sender, recipient),
        (subject2, message2, sender, recipient),
    )
    """
    data_tuple = ((add_prefix(d[0]), d[1], d[2], d[3]) for d in data_tuple)
    send_mass_mail(data_tuple)


@db_flush
@app.task()
def send_password_rest_link(
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None
):
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    subject = '{}{}'.format(EMAIL_SUBJECT_PREFIX, subject)
    body = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
