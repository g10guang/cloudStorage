#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-22 11:22
from app.models.file import File


def filter_file_id(file_ids, user_id):
    """
    过滤掉不属于当前用户的 file id
    :param file_ids: 文件的 id
    :param user_id: 用户 id
    :return:
    """
    file_ids_for_user = []
    for item, in File.query.filter(File.id.in_(file_ids)).filter(File.user_id == user_id).with_entities(File.id):
        file_ids_for_user.append(item)
    return file_ids_for_user
