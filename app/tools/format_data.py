#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-22 10:04
# 拼接数据，用于前后端交互
# 添加使用 uid 原因：前后端接口不对，前段需要通过唯一 id 来区分选择，后台将文件和文件夹分开，无法为前端生成唯一的 id，所以这里为每一个 item 添加一个 uuid 属性


def format_directory(directory):
    """
    将文件夹格式转化为 json key-value
    :param directory:
    :return:
    """
    if directory:
        # type == 1 为文件夹
        # data = {'id': directory.id, 'name': directory.name, 'modifiedTime': directory.modifiedTime.strftime('%Y-%m-%d'), 'type': 1, 'size': 0, 'uid': uuid.uuid4().hex}
        data = {'id': directory.id, 'name': directory.name, 'modifiedTime': directory.modifiedTime.strftime('%Y-%m-%d'), 'type': 1, 'size': 0}
        return data


def format_dirs(dirs):
    """
    将 directories 转化为
    :param dirs:
    :return:
    """
    data = []
    for directory in dirs:
        data.append(format_directory(directory))
    return data


def format_file(file):
    """
    将文件格式转化为 json key-value
    :param file:
    :return:
    """
    if file:
        # type == 0　为文件
        # data = {'id': file.id, 'name': file.name, 'modifiedTime': file.modifiedTime.strftime('%Y-%m-%d'), 'size': file.size, 'type': 0, 'uid': uuid.uuid4().hex}
        data = {'id': file.id, 'name': file.name, 'modifiedTime': file.modifiedTime.strftime('%Y-%m-%d'), 'size': file.size, 'type': 0}
        return data


def format_files(files):
    """
    转化 files list[File] 为 json key-value 格式
    :param files:
    :return:
    """
    data = []
    for file in files:
        data.append(format_file(file))
    return data


def combine_dir_file_into_filelists(dirs, files):
    """
    将 dirs files 拼接到一个 list 中
    :param dirs:
    :param files:
    :return:
    """
    filelists = []
    for folder in dirs:
        filelists.append(format_directory(folder))
    for file in files:
        filelists.append(format_file(file))
    return filelists


