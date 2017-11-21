#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 14:07
# 处理数据库中逻辑中文件操作

from app import app
from flask import g, request, session, jsonify
from app.models.directory import Directory
from flask_login import login_required


@app.route('/add_folder')
@login_required
def add_folder():
    """
    新建文件夹
    :return:
    """
    parent_id = g.args.get('parentFolderId', None, type=int)
    name = g.args.get('name')
    new_dir = Directory(name=name, parent_id=parent_id if parent_id else None, user_id=g.user.id)
    if new_dir.save():
        return jsonify({'status': 1})
    else:
        # 父文件夹有重名文件夹或者文件
        return jsonify({'status': 0})


@app.route('/get_download_ids')
def getDownloadIds():
    return jsonify({'ids': [1, 2, 3]})



