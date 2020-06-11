"""
 -*- coding: utf-8 -*-
 Created on 2020/6/9 17:26
 microblog
 @Author  : Zhouy
 @Blog    : blog.crocodilezs.top

"""

from app import app, db
from app.models import User, Post

@app.shell_context_processor # 装饰器将该函数注册为一个shell上下文函数。
# 当 flask shell 命令运行时，它会调用这个函数并在shell会话中注册它返回的项目。
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post}