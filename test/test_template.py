# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/22 19:45]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Doraemon.settings")
django.setup()

from django.template import Template, Context

txt = """
{{ name }}
{{ email }}
"""

if __name__ == '__main__':
    t = Template(txt)
    c = Context({"name": "Jeeyshe", "email": "Jeeyshe@gmail.com"})
    print(t.render(c))

