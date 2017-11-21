#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 14:09
# 文件的下载传动作

from app import app
from flask import g, request, session, make_response, send_from_directory, send_file


@app.route('/download')
def download():
    """
    给客户端传送文件
    :return:
    """


# @app.route('/download2')
# # @login_required
# def download_file():
#     # with open('/home/g10guang/Pictures/collections/giphy.gif', 'rb') as f:
#     #     response = make_response(f.read())
#     #     response.headers['Content-Type'] = 'image/gif'
#     #     response.headers['Content-Disposition'] = 'attachment; filename=img.gif'
#     #     return response
#     return send_from_directory('/home/g10guang/PycharmProjects/courses/database/oss/storage', '禾芒团队介绍.md')


@app.route('/download_file')
def download2():
    import random
    response = make_response(send_file('/home/g10guang/Pictures/collections/optimized-homer-simpson-t-shirts-woo-hoo.jpg',
                     as_attachment=True, attachment_filename='hello.md', mimetype='image/jpeg'))
    response.headers['Filename'] = str(random.randint(0, 100))
    return response