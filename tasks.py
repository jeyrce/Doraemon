# coding=utf-8
"""
__purpose__ = 基于invoke的常用快捷命令
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/14 21:48]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import os
from invoke import task

root = os.path.dirname(os.path.abspath(__file__))
project = 'Doraemon'


@task
def clean(ctx):
    """--clean trash files"""
    files = [
        "_build",
        "build",
        "dist",
        "*.log",
        "*.pyc",
        "*.sqlite3",
        "*.xls",
        "__pycache__",
    ]
    [ctx.run(f"find . -name '{file}'| xargs rm -rf", echo=True) for file in files]


@task
def check(ctx, j=4):
    """--pylint check"""
    ctx.run(
        f"pylint -j {j} --output-format colorized   --disable=all --enable=E,F {project}"
    )


@task
def install(ctx):
    """--install requirements"""
    file = "requirements.txt.lock" if os.path.exists(
        os.path.join(root, "requirements.txt.lock")
    ) else "requirements.txt"
    ctx.run(f'pip install -r {file} --no-cache', echo=True)


@task
def lock(ctx):
    """--lock requirements"""
    cmds = [
        'pip freeze > requirements.txt',
        'rm -rf requirements.txt.lock',
        'pip-compile --generate-hashes --allow-unsafe requirements.txt -o requirements.txt.lock'
    ]
    [ctx.run(cmd, echo=True) for cmd in cmds]


@task
def version(ctx, new):
    """
    -- change current version to new
    """
    files = [
        ".bumpversion.cfg",
        "VERSION",
        "Doraemon/settings.py",
    ]
    ctx.run(f"bumpversion --new-version {new} {' '.join(files)}", echo=True)
