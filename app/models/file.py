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
    dir = db.relationship('Directory', back_populates='files')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='files')
    modifiedTime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    size = db.Column(db.Integer, nullable=False)
    is_del = db.Column(db.Integer, nullable=False, default=0)
    storage_file_id = db.Column(db.Integer, db.ForeignKey('storage_file.id'))
    storage_file = db.relationship('StorageFile', back_populates='files')

    def __int__(self, name, parent_id, user_id, size, storage_file_id):
        self.name = name
        self.parent_id = parent_id
        self.user_id = user_id
        self.size = size
        self.storage_file_id = storage_file_id

    def save(self, commit=True):
        """
        持久化文件对象
        :return:
        """
        # 检测是否重名，如果重名替换原来的名字
        is_duplicate, new_name = logic_file_tool.check_is_duplicate_name_and_generate_new_name(self.user_id, self.parent_id, self.name)
        if is_duplicate == 1:
            return False
        if is_duplicate == 2:
            self.name = new_name
        db.session.add(self)
        if commit:
            db.session.commit()
        return True

    def delete(self, commit=True):
        """
        删除文件对象
        :return:
        """



from app.tools import logic_file_tool
