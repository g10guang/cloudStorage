#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 20:39

from app import db


class StorageFile(db.Model):
    """
    存储在物理上的文件
    """
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(255), primary_key=True)

    files = db.relationship('File', back_populates='storage_file', lazy='dynamic', cascade='save-update')