"""
 -*- coding: utf-8 -*-
 Created on 2020/6/9 19:53
 config
 @Author  : Zhouy
 @Blog    : blog.crocodilezs.top

"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # 第一项查找环境变量SECRET_KEY的值，第二个项是一个硬编码的字符串。
    # 这种首先检查环境变量中是否有这个配置，找不到的情况下就使用硬编码字符串的配置变量的模式
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 设置数据发生变更后是否发送信号给应用