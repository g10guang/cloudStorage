#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 14:09
# 文件的下载传动作

from app import app
from flask import g, request, session, make_response, send_file, jsonify
from flask_login import login_required
from app.models.file import File
import os
from werkzeug.urls import url_quote
from app.tools import split_data
from app.tools import logic_file_tool
from app.tools import filter_data


@app.route('/download_file')
@login_required
def download():
    """
    给客户端传送文件
    :return:
    """
    file_id = g.args.get('id', type=int)
    if not file_id:
        # 参数中没有附带具体需要下载的文件的 id
        return jsonify({'status': 2}), 400
    file = File.query.get(file_id)
    if not file:
        # 需要下载的文件不存在
        return jsonify({'status': 3}), 404
    # 判断文件是否属于当前用户
    if file.user_id != g.user.id:
        return jsonify({'sttatus': 3}), 403
    storage_file = file.storage_file
    file_in_disk = os.path.join(app.config['UPLOAD_FOLDER'], storage_file.sum, str(storage_file.name))
    filename_in_utf8 = url_quote(file.name)
    response = make_response(send_file(file_in_disk, mimetype=storage_file.content_type, as_attachment=True, attachment_filename=filename_in_utf8))
    response.headers['Filename'] = filename_in_utf8
    return response


@app.route('/get_download_files', methods=['POST'])
@login_required
def get_download_files():
    itmes = g.json['files']
    dirs, files = split_data.split_file_dir(itmes)
    filelist = filter_data.filter_file_id(files, g.user.id)
    fileset = logic_file_tool.get_fileid_in_dirs(dirs)
    fileset.update(filelist)
    return jsonify({'ids': list(fileset)})