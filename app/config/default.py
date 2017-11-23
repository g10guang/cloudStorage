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

    OSS_MODE = os.environ.get('OSS_MODE', 'DEVELOP')

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/oss?charset=utf8'.format(
        MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT)

    STORAGE_PATH = os.environ.get('OSS_STORAGE_PATH', os.path.abspath(os.path.join(os.path.curdir, 'storage')))

    if not os.path.exists(STORAGE_PATH):
        os.mkdir(STORAGE_PATH)

    JWT_ISS = 'whoyoungblog'

    JWT_AUD = 'oss'

    # 用于 JWT 加密的 secret_key
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    # 一个 Sqlalchemy 未来删去的特性，需要声明该配置去压制 suppress
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_SECRET_KEY_FILE = 'blog_secret_key'

    # 控制上传的文件最大为 100MB
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024 * 1024

