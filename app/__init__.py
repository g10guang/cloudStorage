#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 11:58

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from app.config import load_config


config = load_config()

if not os.path.exists(config.SESSION_SECRET_KEY_FILE):
    with open(config.SESSION_SECRET_KEY_FILE, 'wb') as f:
        f.write(os.urandom(24))


app = Flask('oss')

app.config.from_object(config)

with open(config.SESSION_SECRET_KEY_FILE, 'rb') as f:
    # 多个 app 需要共享一个 secret_key 从而达到共享 session 信息
    app.secret_key = f.read()

db = SQLAlchemy(app)

login_manager = LoginManager(app)

# import views
from app.apis import verify, download, upload, logic_operation

# import models
from app.models import directory, file, storage_file, user