#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 12:10

from app.config.default import DefaultConfig


class DevelopConfig(DefaultConfig):
    """
    开发配置
    """
    DEBUG = True