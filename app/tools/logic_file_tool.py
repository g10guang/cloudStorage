#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-20 21:03
# 进行关于用户逻辑上的文件操作

from app.models.directory import Directory
from app.models.file import File
from flask import g
import re


def check_is_duplicate_name_and_generate_new_name(user_id, parent_id, name):
    """
    检测某个用户目录下是否存在同名文件或者文件夹，
    以及该父文件夹是否是当前用户的
    如果存在同名，则更换名字
    :param user_id: 用户 id
    :param parent_id: 父级目录id，如果是顶级目录，则 parent_id is None
    :param name: 检测的名字
    :return: (status_code, new_name)
    0 ==> 该文件夹下不存在 name 名的文件或者文件夹
    1 ==> 该文件夹不是当前用户所拥有
    2 ==> 当前目录下已存在同名文件或者文件夹
    如果名字不冲突，那么 new_name == name
    """
    # 编译可复用的正则匹配对象
    t = re.compile(r'{name}\((\d+)\)'.format(name=name))
    # 创建集合
    indexes_used = set()
    # 标识是否重名了
    is_duplicate_name = False
    if parent_id:
        # 不是根目录
        parent = Directory.query.get(parent_id)
        # 判断用户是否拥有当前目录
        if not parent.user_id == user_id:
            # 父文件夹不是 current_user 所拥有
            return 1, None
        for subdir in parent.dirs:
            if subdir.name == name:
                is_duplicate_name = True
            else:
                # 寻找已经使用了的下标
                for index in t.findall(subdir.name):
                    indexes_used.add(index)
        for subfile in parent.files:
            if subfile.name == name:
                is_duplicate_name = True
            else:
                for index in t.findall(subfile.name):
                    indexes_used.add(index)
    else:
        # 是根目录，查找该用户根目录下的所有文件和文件夹
        dirs_in_root = Directory.query.filter(Directory.user_id == user_id).filter(Directory.parent_id.is_(None))
        for subdir in dirs_in_root:
            if subdir.name == name:
                is_duplicate_name = True
            else:
                for index in t.findall(subdir.name):
                    indexes_used.add(index)
        files_in_root = File.query.filter(File.user_id == user_id).filter(File.parent_id.is_(None))
        for subfile in files_in_root:
            if subfile.name == name:
                is_duplicate_name = True
            else:
                for index in t.findall(subfile.name):
                    indexes_used.add(index)
    if not is_duplicate_name:
        # 文件夹下没有重名
        return 0, name
    else:
        # 文件夹下重名了，为当前文件生成新的文件名
        new_name = generate_new_name_with_index(name, indexes_used)
        return 2, new_name


def is_parent_dir_belong_to_current_user(parent_id):
    """
    判断 parent_id 所指向的文件夹是否属于当前用户
    :param parent_id: 父文件夹 id
    :return:
    """
    if not parent_id:
        return True
    user_id = Directory.query.with_entities(Directory.user_id).filter(Directory.id == parent_id).one()[0]
    if user_id == g.user.id:
        return True
    else:
        return False


def generate_new_name_with_index(old_name, indexes_used):
    """
    由于文件名冲突了，所以为用户生成一个带后缀的新文件名 name(i)
    :param old_name:
    :param indexes_used:
    :return:
    """
    index = 1
    while True:
        if str(index) not in indexes_used:
            return '{name}({index})'.format(name=old_name, index=index)
        index += 1


def check_is_duplicate(user_id, parent_id, name):
    """
    检测某个用户目录下是否存在同名文件或者文件夹，
    以及该父文件夹是否是当前用户的
    如果存在同名，则更换名字
    :param user_id: 用户 id
    :param parent_id: 父级目录id，如果是顶级目录，则 parent_id is None
    :param name: 检测的名字
    :return:
    0 ==> 该文件夹下不存在 name 名的文件或者文件夹
    1 ==> 该文件夹不是当前用户所拥有
    2 ==> 当前目录下已存在同名文件或者文件夹
    """
    # 标识是否重名了
    is_duplicate_name = False
    if parent_id:
        # 不是根目录
        parent = Directory.query.get(parent_id)
        # 判断用户是否拥有当前目录
        if not parent.user_id == user_id:
            # 父文件夹不是 current_user 所拥有
            return 1
        for subdir in parent.dirs:
            if subdir.name == name:
                is_duplicate_name = True
        for subfile in parent.files:
            if subfile.name == name:
                is_duplicate_name = True
    else:
        # 是根目录，查找该用户根目录下的所有文件和文件夹
        dirs_in_root = Directory.query.filter(Directory.user_id == user_id).filter(Directory.parent_id.is_(None))
        for subdir in dirs_in_root:
            if subdir.name == name:
                is_duplicate_name = True
        files_in_root = File.query.filter(File.user_id == user_id).filter(File.parent_id.is_(None))
        for subfile in files_in_root:
            if subfile.name == name:
                is_duplicate_name = True
    return 2 if is_duplicate_name else 0