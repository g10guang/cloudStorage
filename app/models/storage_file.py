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
    sum = db.Column(db.String(40))
    name = db.Column(db.Integer)
    # content-type 主要用于传输过程中设置头信息
    content_type = db.Column(db.String(50))
    size = db.Column(db.Integer)
    files = db.relationship('File', back_populates='storage_file', lazy='dynamic', cascade='save-update')

    def __init__(self, sum, name, content_type, size):
        self.sum = sum
        self.name = name
        self.content_type = content_type
        self.size = size

    def save(self, commit=True):
        """
        持久化该对象
        :return:
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return True