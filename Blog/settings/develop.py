#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2020/1/15 20:44
"""开发环境的配置"""

from .base import *  # NOQA


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Blogs',
        'USER': 'root',
        'PASSWORD': '000000',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': None,
    }
}