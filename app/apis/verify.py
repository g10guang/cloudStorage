#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 10:29
# function: 验证用户身份

import jwt

from app import app
from flask import g, jsonify, make_response, send_file, send_from_directory, session
from app.models.user import User
from flask_login import login_user, login_required


@app.route('/jwt_verify')
def jwt_verify():
    """
    验证用户 jwt 信息
    :return:
    """
    token = g.args['jwt']
    try:
        msg = jwt.decode(token, key=app.config['JWT_SECRET_KEY'], audience=app.config['JWT_AUD'], issuer=app.config['JWT_ISS'])
    except jwt.ExpiredSignatureError:
        # JWT 过期
        return jsonify({'status': 0})
    uid = msg['uid']
    user = User.query.filter_by(uid=uid).first()
    if user:
        # 找到 user
        login_user(user, remember=True)
        return jsonify({'status': 1})
    else:
        # 没能加载出用户
        return jsonify({'status': 2})


