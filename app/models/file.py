#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 20:38

from app import db
import datetime


class File(db.Model):
    __tablename__ = 'file'

    """
    逻辑概念上的文件类型
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.String, db.ForeignKey('dir.id'))
    dir = db.relationship('Directory', back_populates='files', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='files', lazy='dynamic')
    modifiedTime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    size = db.Column(db.Integer, nullable=False)
    is_del = db.Column(db.Integer, nullable=False, default=0)
    storage_file_id = db.Column(db.Integer, db.ForeignKey('storage_file.id'))
    storage_file = db.relationship('StorageFile', back_populates='files', lazy='dynamic')