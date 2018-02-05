#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-22 11:23
# 用于分离数据，大部分用于和前端交互使用


def split_file_dir(items):
    """
    items 为　dir 和　file 混杂的数组，需要分开 dir 和 file
    :param files:
    :return: (dirs, files) 两个属性都是 set
    """
    files = set()
    dirs = set()
    for item in items:
        if item['type'] == 1:
            dirs.add(item['id'])
        elif item['type'] == 0:
            files.add(item['id'])
    return dirs, files
