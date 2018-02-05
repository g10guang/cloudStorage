#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 12:09
import os


def load_config():
    mode = os.environ.get('OSS_MODE', 'DEVELOP')
    try:
        if mode == 'PRODUCT':
            from app.config.product import ProductConfig
            return ProductConfig
        else:
            # 开发配置
            from app.config.develop import DevelopConfig
            return DevelopConfig
    except ImportError:
        from app.config.default import DefaultConfig
        return DefaultConfig

