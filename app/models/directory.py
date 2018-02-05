#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-18 20:55

from app import db
import datetime
from flask import g
from app.models.file import File


class Directory(db.Model):
    """
    文件夹
    """
    __tablename__ = 'dir'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    modifiedTime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    parent_id = db.Column(db.Integer, db.ForeignKey('dir.id'), default=None)
    # 子文件夹
    dirs = db.relationship('Directory', back_populates='parent_dir', lazy='dynamic')
    # 父文件夹
    parent_dir = db.relationship('Directory', back_populates='dirs', remote_side=[id])

    # 不能够设置 delete-orphan，因为顶级文件没有 parent，设置级联删除，如果不设置级联删除，有可能文件会变为根目录下的文件
    # cascade: all, delete-orphan == save-update, merge, delete, refresh-expire, expunge, delete-orphan
    # save-update 当一个 object 加入到 session 后，其对应的关系也自动加入到 session 中
    # merge:
    # delete: 父被标示别删除，子也被标示为删除
    # refresh-expire:
    # expunge:
    # delete-orphan: 当子与父接触关系后，删除子
    files = db.relationship('File', back_populates='dir', cascade='save-update', lazy='dynamic')
    is_del = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='dirs')

    def __init__(self, name, parent_id, user_id):
        self.name = name
        self.parent_id = parent_id
        self.user_id = user_id

    def save(self, commit=True):
        """
        持久化一个文件夹，但是会在初始化前做检验是否存在同名文件或者文件夹
        :param commit:
        :return:
        """
        is_duplicate = logic_file_tool.check_is_duplicate(self.user_id, self.parent_id, self.name)
        if not is_duplicate:
            db.session.add(self)
            if commit:
                db.session.commit()
            return True
        return False


from app.tools import logic_file_tool
