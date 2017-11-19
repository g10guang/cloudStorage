#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 12:10
import os


class DefaultConfig:
    """
    默认配置信息
    """
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME')

    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

    MYSQL_HOST = os.environ.get('MYSQL_HOST')

    MYSQL_PORT = os.environ.get('MYSQL_PORT')

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/oss?charset=utf8'.format(
        MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT)
