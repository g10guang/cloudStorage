#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 12:10

from app.config.default import DefaultConfig
import os


class ProductConfig(DefaultConfig):
    """
    产品配置
    """
    DEBUG = False

    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.curdir), 'storage')