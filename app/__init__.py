#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 11:58

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import load_config

config = load_config()

app = Flask('oss')

app.config.from_object(config)

db = SQLAlchemy(app)