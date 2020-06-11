"""
 -*- coding: utf-8 -*-
 Created on 2020/6/9 17:18
 routes
 @Author  : Zhouy
 @Blog    : blog.crocodilezs.top

"""
# 视图函数
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import EditProfileForm

@app.route('/') # 装饰器，装饰器会修改跟在其后的函数。装饰器的常见模式是使用它们将函数注册为某些事件的回调函数
# 在这种情况下，＠app.route修饰器在作为参数给出的URL和函数之间创建一个关联。
# 在这个例子中，有两个装饰器，它们将URL /和/index索引关联到这个函数。
# 这意味着，当Web浏览器请求这两个URL中的任何一个时，Flask将调用该函数并将其返回值作为响应传递回浏览器。这样做是为了在运行这个应用程序的时候会稍微有一点点意义。
@app.route('/index')
@login_required
# 视图函数
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was cool!'
        }
    ]
    return render_template('index.html', title='Home', posts = posts)

@app.route('/login', methods=['GET', 'POST']) # 告诉Flask这个视图函数接受GET和POST请求，并覆盖了默认的GET
# 当浏览器向服务器提交表单数据时，通常会使用POST请求
def login():
    """
    form = LoginForm()
    if form.validate_on_submit():# 执行校验操作
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))# flash()函数是向用户显示消息的有效途径。许多应用使用这个技术来让用户知道某个动作是否成功
        return redirect(url_for('index'))# 指引浏览器自动重定向到它的参数所关联的URL。
    return render_template('login.html', title='Sign In', form=form)
    """
    if current_user.is_authenticated: # 若用户已经登录
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # 若用户提交合法
        user = User.query.filter_by(username=form.username.data).first() # 根据用户名查找数据库，当只需要一个结果的时候，使用.first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
# 将模板转换为完整的html页面的操作成为渲染。为了渲染模板，需要从Flask框架中导入一个名为render_template()的函数。
# 该函数需要传入模板文件名和模板参数的变量列表，并返回模板中所有占位符都用实际变量值替换后的字符串结果。

@app.route('/register', methods=['GET', 'POST'])
def register():#视图函数
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)