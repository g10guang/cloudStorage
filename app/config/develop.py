#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 12:10

from app.config.default import DefaultConfig
import os


class DevelopConfig(DefaultConfig):
    """
    开发配置
    """
    DEBUG = True

    # 文件上传保存路径
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.curdir), 'storage')

    # 用于显示　sql 语句
    SQLALCHEMY_ECHO = True
