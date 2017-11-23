#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-20 21:03
# 进行关于用户逻辑上的文件操作

from app.models.directory import Directory
from app.models.file import File
from flask import g
import re
from app import db
import datetime
from sqlalchemy import desc


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
    re_statement = re.compile(r'^{name}(\((\d+)\))?$'.format(name=name))
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
            if regex_match_index_into_set(re_statement, subdir.name, indexes_used) == 1:
                is_duplicate_name = True
        for subfile in parent.files:
            if regex_match_index_into_set(re_statement, subfile.name, indexes_used) == 1:
                is_duplicate_name = True
    else:
        # 是根目录，查找该用户根目录下的所有文件和文件夹
        dirs_in_root = Directory.query.filter(Directory.user_id == user_id).filter(Directory.parent_id.is_(None))
        for subdir in dirs_in_root:
            if regex_match_index_into_set(re_statement, subdir.name, indexes_used) == 1:
                is_duplicate_name = True
        files_in_root = File.query.filter(File.user_id == user_id).filter(File.parent_id.is_(None))
        for subfile in files_in_root:
            if regex_match_index_into_set(re_statement, subfile.name, indexes_used) == 1:
                is_duplicate_name = True
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


def is_belong_to_user(item, user_id):
    """
    判断当前文件是否属于 current_user
    :param item:
    :return:
    """
    if item.user_id == user_id:
        return True
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
    if parent_id:
        # 不是根目录
        parent = Directory.query.get(parent_id)
        # 判断用户是否拥有当前目录
        if not parent.user_id == user_id:
            # 父文件夹不是 current_user 所拥有
            return 1
        for subdir in parent.dirs:
            if subdir.name == name:
                return 2
        for subfile in parent.files:
            if subfile.name == name:
                return 2
    else:
        # 是根目录，查找该用户根目录下的所有文件和文件夹
        dirs_in_root = Directory.query.filter(Directory.user_id == user_id).filter(Directory.parent_id.is_(None))
        for subdir in dirs_in_root:
            if subdir.name == name:
                return 2
        files_in_root = File.query.filter(File.user_id == user_id).filter(File.parent_id.is_(None))
        for subfile in files_in_root:
            if subfile.name == name:
                return 2
    return 0


def regex_match_index_into_set(re_statement, name, indexes_used):
    """
    使用正则表达式匹配下标以及匹配有没有重复
    :return:
    0 ==> 没有产生冲突　   匹配到 not name
    1 ==> 名字产生了冲突   匹配到 name
    2 ==> 匹配出了　      匹配到 name(i
    """
    result = re_statement.findall(name)
    if not result:
        # result = [] 表明没有匹配上
        return 0
    tmp = result[0][1]
    if len(tmp) == 0:
        return 1
    indexes_used.add(tmp)
    return 2


def list_dir(dir_id, user_id):
    """
    查询某个文件夹下的文件夹和目录
    :param dir_id:
    :param user_id: current_user.id
    :return:
    1 ==> 当前目录不属于该用户
    """
    if not is_parent_dir_belong_to_current_user(dir_id):
        # 当前目录不属于该用户
        return 1, None, None
    if dir_id:
        # 用户访问某个特定目录
        parent_id = dir_id
        sub_dirs = Directory.query.with_entities(Directory.id, Directory.name, Directory.modifiedTime).filter(Directory.parent_id == parent_id).filter(Directory.is_del == 0).order_by(desc(Directory.modifiedTime)).all()
        sub_files = File.query.with_entities(File.id, File.name, File.modifiedTime, File.size).filter(File.parent_id == parent_id).filter(File.is_del == 0).order_by(desc(File.modifiedTime)).all()
    else:
        # 用户访问顶级目录
        parent_id = None
        sub_dirs = Directory.query.with_entities(Directory.id, Directory.name, Directory.modifiedTime).filter(Directory.parent_id == parent_id).filter(Directory.user_id == user_id).filter(Directory.is_del == 0).order_by(desc(Directory.modifiedTime)).all()
        sub_files = File.query.with_entities(File.id, File.name, File.modifiedTime, File.size).filter(File.parent_id == parent_id).filter(File.user_id == user_id).filter(File.is_del == 0).order_by(File.modifiedTime).all()
    return 0, sub_dirs, sub_files


def rename(file_id, user_id, new_name, cls):
    """
    重命名某个文件或文件夹
    :param file_id: 文件 id
    :param user_id: 当前用户 id
    :param new_name: 改名后的名字
    :param cls: 改名的类，可以是 Directory 或者 File
    :return:
    0 ==> 成功更改文件名
    1 => 当前文件不属于当前用户
    2 ==> 新旧名字相同，没有进行任何更改
    3 ==> 新文件名不能为空
    4 ==> 出现同名，不能够重命名
    5 ==> 文件不存在
    """
    if not new_name:
        return 3
    file = cls.query.get(file_id)
    if not file:
        # 文件不存在
        return 5
    if file.name == new_name:
        # 新旧名字相同，没有进行任何更改
        return 2
    tmp = check_is_duplicate(user_id, file.parent_id, new_name)
    if tmp == 1:
        return 1
    elif tmp == 2:
        return 4
    file.name = new_name
    # 将更改时间也更改
    file.modifiedTime = datetime.datetime.now()
    db.session.commit()
    return 0


def get_fileid_in_dir_recursively(directory: Directory, filelsits=set()):
    """
    递归提取 dir 下的所有 file
    :return:
    """
    if not directory or directory.user_id != g.user.id:
        return filelsits
    for item in directory.files.all():
        filelsits.add(item.id)
    for d in directory.dirs:
        get_fileid_in_dir_recursively(d, filelsits)
    return filelsits


def get_fileid_in_dirs(dir_ids):
    """
    获取 dirs 文件下的所有该用户的文件
    :param dir_ids:
    :return:
    """
    fileset = set()
    for did in dir_ids:
        d = Directory.query.filter(Directory.id == did).one()
        get_fileid_in_dir_recursively(d, fileset)
    return fileset


def delete_file_by_id(file_id, user_id=None, commit=True):
    """
    删除文件
    :param file_id: 需要删除的文件 id
    :param user_id: 当前用户 id
    :return:
    0 ==> 成功删除文件
    1 ==> 文件不属于当前用户
    2 ==> 文件原本已经处于被删除状态
    3 ==> 文件不存在
    """
    file = File.query.get(file_id)
    if not file:
        return 3
    if not is_belong_to_user(file, user_id):
        return 1
    if file.is_del == 1:
        return 2
    # 置删除位为 1
    file.is_del = 1
    # 提交文件删除更改
    if commit:
        db.session.commit()
    return 0


def delete_dir_by_id(dir_id, user_id=None, commit=True):
    """
    删除文件夹
    :param dir_id: 需要删除的文件夹 id
    :param user_id: 当前用户 id
    :return:
    0 ==> 成功删除文件夹
    1 ==> 文件夹不属于用户
    2 ==> 文件夹本来已经处于删除状态
    3 ==> 文件不存在
    """
    folder = Directory.query.get(dir_id)
    if not folder:
        return 3
    if not is_belong_to_user(folder, user_id):
        return 1
    if folder.is_del == 1:
        return 2
    # 置删除位为　1
    folder.is_del = 1
    for file in folder.files:
        delete_file_obj(file)
    for subdir in folder.dirs:
        delete_dir_obj(subdir)
    if commit:
        db.session.commit()
    return 0


def delete_file_obj(file):
    """
    删除文件，传递的是　file object
    :param file: 文件对象
    :return:
    """
    if file:
        if file.is_del == 0:
            file.is_del = 1


def delete_dir_obj(folder):
    """
    删除文件夹，传递的是 Directory object
    :param folder: 文件夹对象
    :return:
    """
    if folder:
        if folder.is_del == 0:
            folder.is_del = 1
        else:
            # 该文件夹已经被删除
            return
    for file in folder.files:
        delete_file_obj(file)
    for subdir in folder.dirs:
        delete_dir_obj(subdir)


def delete_dirs_and_files(dir_ids, file_ids, user_id):
    """
    删除多个文件夹和文件
    :param dir_ids: 文件夹 id
    :param file_ids: 文件 id
    :param user_id: 用户 id
    :return:
    """
    for did in dir_ids:
        delete_dir_by_id(did, user_id=user_id)
    for fid in file_ids:
        delete_file_by_id(fid, user_id=user_id)


def move_file_dir_by_id(file_ids, dir_ids, parent_id, user_id, commit=True):
    """
    通过传递 id 来移动文件和文件夹
    :param file_ids:
    :param dir_ids:
    :param parent_id: 需要移动到的目标文件夹
    :param user_id: 当前用户 id
    :return:
    0 ==> 移动完成
    1 ==> parent_id 不存在
    2 ==> parent_folder 不属于当前用户
    """
    duplicate_names = []
    if not parent_id:
        # 移动到根目录
        return move_file_dir_to_root(file_ids, dir_ids, user_id)
    parent_folder = Directory.query.get(parent_id)
    if not parent_folder:
        return 1, duplicate_names
    if parent_folder.user_id != user_id:
        return 2, duplicate_names
    names = get_names_in_dir(parent_folder)
    for did in dir_ids:
        move_dir_by_id(did, parent_folder, user_id, names, duplicate_names)
    for fid in file_ids:
        move_file_by_id(fid, parent_folder, user_id, names, duplicate_names)
    if commit:
        db.session.commit()
    return 0, duplicate_names


def move_dir_by_id(did, parent_obj, user_id, names:set, duplicate_names:list):
    """
    通过文件夹 id 移动单个文件夹
    :param names: parent_folder 名字集合，用于去重
    :param did: 需要移动的文件夹 id
    :param parent_obj: 目标文件夹对象 Directory.id
    :param user_id: 当前用户 id
    :return:
    0 ==> 成功移动
    1 ==> 文件夹不存在
    2 ==> 文件夹不属于当前用户
    3 ==> 重名
    """
    folder = Directory.query.get(did)
    if not folder:
        return 1
    if folder.user_id != user_id:
        return 2
    if folder.name in names:
        duplicate_names.append({'name': folder.name, 'type': 1, 'id': did})
        return 3
    names.add(folder.name)
    parent_id = parent_obj.id if parent_obj else None
    folder.parent_id = parent_id
    return 0


def move_file_by_id(fid, parent_obj, user_id, names: set, duplicate_names:list):
    """
    通过文件 id 移动单个文件
    :param names: parent_folder 下的文件集合，可以用于判断是否出现重复
    :param fid: 需要移动的文件 id
    :param parent_obj: 目标文件夹对象 Directory object
    :param user_id: 当前用户 id
    :return:
    0 ==> 成功移动
    1 ==> 文件不存在
    2 ==> 文件不属于当前用户
    3 ==> 重名
    """
    file = File.query.get(fid)
    if not file:
        return 1
    if file.user_id != user_id:
        return 2
    # 判断是否出现重名情况
    if file.name in names:
        duplicate_names.append({'name': file.name, 'type': 0, 'id': fid})
        return 3
    names.add(file.name)
    parent_id = parent_obj.id if parent_obj else None
    file.parent_id = parent_id
    return 0


def get_names_in_dir(parent_dir, names=set()):
    """
    得到文件夹下的所有文件以及文件夹的名称
    :param names:
    :param parent_dir:
    :return: set() of names of files and dirs
    """
    for subdir in parent_dir.dirs:
        if subdir.is_del == 0:
            names.add(subdir.name)
    for subfile in parent_dir.files:
        if subfile.name == 0:
            names.add(subfile.name)
    return names


def move_file_dir_to_root(file_ids, dir_ids, user_id, commit=True):
    """
    将文件和文件夹移动到该用户的根目录下
    :param file_ids:
    :param dir_ids:
    :param user_id:
    :param commit:
    :return:
    0 ==> 成功移动
    """
    filelist = File.query.filter(File.parent_id.is_(None)).filter(File.user_id == user_id).filter(File.is_del == 0)
    dirlist = Directory.query.filter(Directory.parent_id.is_(None)).filter(Directory.user_id == user_id).filter(Directory.is_del == 0)
    names = set()
    duplicate_names = []
    for item in filelist:
        names.add(item.name)
    for item in dirlist:
        names.add(item.name)
    for did in dir_ids:
        move_dir_by_id(did, None, user_id, names, duplicate_names)
    for fid in file_ids:
        move_file_by_id(fid, None, user_id, names, duplicate_names)
    if commit:
        db.session.commit()
    return 0, duplicate_names