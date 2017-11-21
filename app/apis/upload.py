#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 14:09
# 文件上传动作

import os

from flask import g, request, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app
from app.models.file import File
from app.tools import logic_file_tool
from app.tools import storage_file_tool


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    上传用户上传的文件
    :return:
    """
    file = request.files['file']
    if file:
        # 防止文件名 ../../../.bashrc 等攻击
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'ok'


@app.route('/add_file', methods=['POST'])
@login_required
def add_file():
    parent_id = request.form.get('parentFolderId', None, type=int)
    # 获得上传的文件
    file = request.files['file']
    if not logic_file_tool.is_parent_dir_belong_to_current_user(parent_id):
        # current user 并不拥有 parent_id 目录
        return jsonify({'status': 2})
    if file:
        # 防止文件名 ../../../.bashrc 等攻击
        # filename = secure_filename(file.filename)
        filename = file.filename
        storage_file_id, file_size = storage_file_tool.save_new_hash_file(file)
        newfile = File(name=filename, parent_id=parent_id, user_id=g.user.id, size=file_size, storage_file_id=storage_file_id)
        if newfile.save():
            # 添加成功
            return jsonify({'status': 1, 'name': newfile.name})
        else:
            # 添加失败
            return jsonify({'status': 2})


