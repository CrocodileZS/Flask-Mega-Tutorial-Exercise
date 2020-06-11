"""
 -*- coding: utf-8 -*-
 Created on 2020/6/9 17:11
 __init__
 @Author  : Zhouy
 @Blog    : blog.crocodilezs.top

"""

import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
# 这种注册Flask插件的模式希望你了然于胸，因为大多数Flask插件都是这样初始化的
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'# 'login'是登录视图函数名
bootstrap = Bootstrap(app)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors


# routes模块中有什么？ 路由是应用程序实现的不同url。在Flask中，应用程序路由的处理逻辑被编写为Python函数，成为视图函数。
# 视图函数被映射到一个或多个路由URL，以便Flask知道当客户端请求给定的URL时执行什么逻辑