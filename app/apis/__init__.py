#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 10:29

from app import app, login_manager
from flask import g, request, session
from flask_login import current_user
from app.models.user import User


@app.before_request
def app_before_request():
    """
    处理参数
    :return:
    """
    g.user = current_user
    if request.method == 'GET':
        g.args = request.args
    elif request.method == 'POST':
        g.args = request.json


@app.after_request
def app_after_request(response):
    """
    处理 request 请求后 header 做跨域
    :return:
    """
    # 接受的来源
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    # 允许 js 读取的头
    response.headers['Access-Control-Expose-Headers'] = 'Authorization, Filename'
    # 允许 js 请求的方法
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
    # 接受的头字段
    # X-Requested-With 是 Ajax 请求则会被至为 XMLHttpRequest
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, withCredentials'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)