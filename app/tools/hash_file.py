#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 20:32

import hashlib
from app.tools import storage_file_tool
import os
from app import app


STORAGE_PATH = app.config['UPLOAD_FOLDER']


SIZE_5MB = 5 * 1024 * 1024

SIZE_10MB = SIZE_5MB * 2

SIZE_20MB = SIZE_10MB * 2


def sha1sum_file(stream):
    """
    使用 sha1sum hash 算法计算文件的 hash 值
    读取文件的所有字节，然后再送到 hashlib.sha1sum 中计算
    :return: (hash. size)
    """
    # 记录当前流中指针位置
    mark_position = stream.tell()
    # 计算文件大小
    size = storage_file_tool.calculate_file_size_in_stream(stream)
    sha1 = hashlib.sha1()
    if size <= SIZE_10MB:
        # 文件长度小于 10MB 直接计算 hash
        # 将文件的指针指到头部
        stream.seek(0)
        sha1.update(stream.read())
    else:
        # 只计算前 5MB 和 后 5MB 的 hash 值
        stream.seek(0)
        sha1.update(stream.read(SIZE_5MB))
        stream.seek(SIZE_5MB, os.SEEK_END)
        sha1.update(stream.read())
    # 将文件指针还原
    stream.seek(mark_position)
    return sha1.hexdigest(), size


def sha512_file(stream):
    """
    使用 hashlib.sha512 哈希计算文件的 hash 值
    :param stream: 流对象
    :return: bytearray 记录文件的 hash 值
    """
    sha512 = hashlib.sha512()
    # 记录当前位置 mark_position
    mark_position = stream.tell()
    size = storage_file_tool.calculate_file_size_in_stream(stream)
    if size <= SIZE_20MB:
        stream.seek(0)
        sha512.update(stream.read())
    else:
        # 文件过大，只取前10M和后10M存储
        stream.seek(0)
        sha512.update(stream.read(SIZE_10MB))
        stream.seek(SIZE_10MB, os.SEEK_END)
        sha512.update(stream.read(SIZE_10MB))
    # 文件指针还原
    stream.seek(mark_position)
    return sha512.digest()


def sha512_compare_2_stream(file_in_request, file_in_disk: str):
    """
    比较两个流对象是否相等
    :param file_in_request: 用户 requests 上传的文件 requests.files['file']
    :param file_in_disk: 存储在磁盘上的文件
    :return: True 两文件的 sha512 哈希值相等; False 两文件的 sha512 哈希值不相等
    """
    with open(file_in_disk, 'rb') as f:
        requests_file_hash = sha512_file(file_in_request)
        disk_file_hash = sha512_file(f)
    return True if requests_file_hash == disk_file_hash else False