
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user,login_required
from flask_login import current_user
from app.models import db
from .blueprint import web
from app.forms.auth import *
from app.models.user import User
from app.helper.email import send_email


@web.route('/register', methods=['GET', 'POST'])
def register():
    user_form = RegisterForm(request.form)
    if request.method == 'POST' and user_form.validate():
        with db.auto_commit():
            user_info = User()
            user_info.email=user_form.email.data
            user_info.password=user_form.password.data
            user_info.nickname=user_form.nickname.data
            db.session.add(user_info)
        return redirect(url_for('views.login'))

    return render_template('auth/register.html', form=user_form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        user_email=login_form.email.data
        user_pwd=login_form.password.data
        user = User.query.filter_by(email=user_email).first()
        if user and user.user_check_password(user_pwd):
            remeber_me=login_form.remember_me.data
            login_user(user, remember=remeber_me)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('views.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=login_form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    Email_form = EmailForm(request.form)
    if request.method == 'POST' and Email_form.validate():
        account_email = Email_form.email.data
        user = User.query.filter_by(email=account_email).first_or_404()
        send_email(Email_form.email.data, '重置你的密码',
                   'email/reset_password.html', user=user, token=user.generate_token())
        flash('以发送邮件到你的邮箱，请及时查收')
    return render_template('auth/forget_password_request.html', form=Email_form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    Resetform = ResetPasswordForm(request.form)
    if request.method == 'POST' and Resetform.validate():
        success = User.reset_password(token, Resetform.password1.data)
        if success:
            flash('密码已经更新，请使用新密码登录')
            return redirect(url_for('views.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=Resetform)


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangepasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        now_uid=current_user.id
        old_pwd=form.old_password.data
        new_pwd=form.new_password.data
        new_pwd2=form.new_password2.data
        if current_user.user_check_password(old_pwd):
            with db.auto_commit():
                now_user = User.query.get(now_uid)
                now_user.password = new_pwd
            logout_user()
            flash('您的密码已重置，请使用新密码登录')

        else:
            flash('密码错误，密码更改失败')
    return render_template('auth/change_password.html')


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@web.route('/help')
def help():
    return render_template('help.html')