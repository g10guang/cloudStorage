#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 20:40

from app import db


class User(db.Model):
    """
    用户
    """
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)

    dirs = db.relationship('Directory', back_populates='user', lazy='dynamic', cascade='save-update')

    files = db.relationship('File', back_populates='user', lazy='dynamic', cascade='save-update')