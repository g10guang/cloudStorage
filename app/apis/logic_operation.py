#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 14:07
# 处理数据库中逻辑中文件操作

from flask import g, jsonify
from flask import redirect, url_for
from flask_login import login_required

from app import app
from app.models.directory import Directory
from app.models.file import File
from app.tools import format_data
from app.tools import logic_file_tool
from app.tools import split_data
from app.tools import filter_data


@app.route('/add_folder', methods=['GET'])
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
        return jsonify({'status': 1, 'folderInfo': format_data.format_directory(new_dir)})
    else:
        # 父文件夹有重名文件夹或者文件
        return jsonify({'status': 0})


@app.route('/get_cloud_files')
@login_required
def list_dir():
    """
    展示当前文件夹中的文件夹和文件内容
    :return:
    """
    dir_id = g.args.get('parentFolderId', None, type=int)
    status_code, sub_dirs, sub_files = logic_file_tool.list_dir(dir_id, g.user.id)
    if status_code == 1:
        # 该目录不属于当前用户
        return jsonify({'status': 2}), 403
    return jsonify({'fileList': format_data.combine_dir_file_into_filelists(sub_dirs, sub_files)})


@app.route('/rename_file', methods=['GET'])
@login_required
def rename_file():
    """
    重命名某个文件
    :return:
    """
    file_id = g.args.get('id', None, type=int)
    new_name = g.args.get('name')
    status_code = logic_file_tool.rename(file_id, g.user.id, new_name, File)
    if status_code == 0:
        # 成功修改名字
        return jsonify({'status': 1})
    elif status_code == 1:
        # 文件夹不属于当前用户
        return jsonify({'status': 2}), 403
    elif status_code == 2:
        # 新旧文件夹命名相同
        return jsonify({'status': 3})
    elif status_code == 3:
        # 新文件名为空
        return jsonify({'status': 4}), 400
    elif status_code == 4:
        # 父目录出现同名
        return jsonify({'status': 5}), 400
    elif status_code == 5:
        # 文件不存在
        return jsonify({'status': 6}), 400


@app.route('/rename_dir')
@login_required
def rename_dir():
    """
    重命名某个文件夹
    :return:
    """
    dir_id = g.args.get('id', None, type=int)
    new_name = g.args.get('name')
    status_code = logic_file_tool.rename(dir_id, g.user.id, new_name, Directory)
    if status_code == 0:
        # 成功修改名字
        return jsonify({'status': 1})
    elif status_code == 1:
        # 文件夹不属于当前用户
        return jsonify({'status': 2}), 403
    elif status_code == 2:
        # 新旧文件夹命名相同
        return jsonify({'status': 3})
    elif status_code == 3:
        # 新文件名为空
        return jsonify({'status': 4}), 400
    elif status_code == 4:
        # 父目录出现同名
        return jsonify({'status': 5}), 400
    elif status_code == 5:
        # 文件不存在
        return jsonify({'status': 6}), 400


@app.route('/rename')
@login_required
def rename():
    """
    该接口可以修改文件过着文件夹的内容
    :return:
    """
    rename_type = g.args.get('type', 0, type=int)
    if rename_type == 0:
        return redirect(url_for('rename_file', id=g.args['id'], name=g.args['name']))
    elif rename_type == 1:
        return redirect(url_for('rename_dir', id=g.args['id'], name=g.args['name']))
    # type 参数传递错误
    return jsonify({'status': 2})


@app.route('/delete_files', methods=['POST'])
@login_required
def delete():
    """
    删除文件或者文件夹
    :return:
    """
    items = g.json['files']
    dirs, files = split_data.split_file_dir(items)
    logic_file_tool.delete_dirs_and_files(dirs, files, g.user.id)
    return jsonify({'status': 1})


@app.route('/move', methods=['POST'])
def move():
    """
    移动文件或者文件夹
    :return:
    """
    # 需要被移动的文件和文件夹
    items = g.json['files']
    # 移动到的目标文件夹
    parent_id = g.json.get('targetParentId')
    if not isinstance(parent_id, int):
        return jsonify({'status': 2}), 400
    dirs, files = split_data.split_file_dir(items)
    logic_file_tool.move_file_dir_by_id(files, dirs, parent_id, user_id=g.user.id)
    return jsonify({'status': 1})