#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 20:53
import os

from app import app
from app.models.storage_file import StorageFile
from app.tools import hash_file


STORAGE_PATH = app.config['UPLOAD_FOLDER']


def calculate_file_size_in_stream(stream):
    """
    Flask request 接收到文件二进制流，在流中计算文件长度
    :param stream: 流，可以是文件流或者是 StringIO BytesIO 等
    :return:
    """
    # 记录当前位置
    now_position = stream.tell()
    # 通过移动流指针计算文件大小
    stream.seek(0)
    size = stream.seek(0, os.SEEK_END)
    # 移动到原来的位置
    stream.seek(now_position)
    return size


def check_is_hash_file_exists(hash_val: str) -> bool:
    """
    检测云盘上是否有相同 hash 的文件了
    :param hash_val: 文件的 hash 值
    :return:
    """
    # 判断该 hash_val 的文件夹是否存在
    if os.path.exists(os.path.join(STORAGE_PATH, hash_val)):
        return True
    else:
        return False


def store_file_in_hashdir(file, hash_val, file_size):
    """
    检测该文件是否已经存在与物理磁盘上
    :param file: 文件对象
    :param hash_val: 文件的 hash 值
    :param file_size: 文件大小
    :return:
    """
    with_same_size = False
    hash_dir = os.path.join(STORAGE_PATH, hash_val)
    files_with_same_hash = StorageFile.query.filter(StorageFile.sum == hash_val).with_entities(StorageFile.name, StorageFile.size, StorageFile.id)
    # 记录当前最大 name
    max_name = 0
    same_name = 0
    storage_file_id = None
    # 查找是否拥有相同 size 的
    for t_name, t_size, t_id in files_with_same_hash:
        if max_name < t_name:
            max_name = t_name
        if t_size == file_size:
            with_same_size = True
            same_name = t_name
            storage_file_id = t_id
            break
    if with_same_size:
         # 需要进一步进行比较
        is_same = hash_file.sha512_compare_2_stream(file.stream, os.path.join(hash_dir, str(same_name)))
         # 如果两文件不相等，再存储一份；如果两文件相等，则不进行存储
        if not is_same:
            # 两文件不相等
            storage_file_id = save_storage_file(file.content_type, file, hash_val, file_size, max_name + 1)
    else:
        # 直接存储
        storage_file_id = save_storage_file(file.content_type, file, hash_val, file_size, max_name + 1)
    return storage_file_id


def save_new_hash_file(file):
    """
    保存用户新上传的文件
    :param file: requests.files['file'] 提取出来的文件对象
    :return: (存储在物理磁盘文件的id, file文件大小)
    """
    hash_val, file_size = hash_file.sha1sum_file(file.stream)
    if check_is_hash_file_exists(hash_val):
        storage_file_id = store_file_in_hashdir(file, hash_val, file_size)
    else:
        # 如果文件夹还不存在就创建该文件夹
        os.mkdir(os.path.join(STORAGE_PATH, hash_val))
        # 存储该文件到磁盘
        storage_file_id = save_storage_file(file.content_type, file, hash_val, file_size, 1)
    return storage_file_id, file_size


def save_storage_file(content_type, file, hash_val, file_size, name):
    """
    持久化一个 storage_file 并且保存文件到磁盘
    :param content_type:
    :param file:
    :param hash_val:
    :param file_size:
    :param name:
    :return: 数据库中对应文件 storage_file 的 id
    """
    storage_file = StorageFile(hash_val, name, content_type, file_size)
    storage_file.save()
    # 将文件保存到物理磁盘
    file.save(os.path.join(STORAGE_PATH, hash_val, str(name)))
    return storage_file.id

