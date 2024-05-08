import forms.formdef as forms
import os

from backend.profile.file_manager import *
from backend.database import Database
from flask import Flask, url_for, redirect, request, render_template, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

# DEPLOY CONFIG
from config import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# EXTERNAL ROUTES
app.add_url_rule('/files', methods=['GET', 'POST'], view_func=file_handling)
app.add_url_rule('/download/<filename>', view_func=download_file)
app.add_url_rule('/delete/<filename>', methods=['GET', 'POST'], view_func=delete_file)


# INTERNAL ROUTES
@login_manager.user_loader
def load_user(user_id):
    return Database.get_user_by_id(user_id=user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('file_handling'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.is_submitted():
        username, password = form.username.data, form.password.data
        if Database.validate_login_by_username(username, password):
            user = Database.get_user_by_username(username)
            login_user(user)
            return redirect(url_for('file_handling'))
        else:
            flash('Неверное имя пользователя или пароль')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''

    form = forms.RegistrationForm()
    if form.is_submitted():
        username, email, password_1, password_2 = form.username.data, form.email.data, form.password_1.data, form.password_2.data
        if password_1 == password_2:
            message, success = Database.register_user(username, password_1, email)
            if success:
                return redirect(url_for('login'))
            else:
                error = message
        else:
            error = "Пароли не совпадают"

    return render_template('register.html', form=form, error=error)


@app.route('/Personal_Page')
def Profile():
    return render_template('Personal_Page.html')


# ENTRYPOINT
def deploy_web(host="127.0.0.1", port=80, debug=False):
    app.run(host=host, port=port, debug=debug)


@app.route('/settings')
def settings():
    return render_template('settings.html')


def update_login(new_login):
    if new_login != '' and not new_login_exists(new_login):
        print("Login updated to:", new_login)
        return True
    return False


def update_password(old_password, new_password, confirm_new_password):
    user_password_hash = get_user_password()
    if not check_password_hash(user_password_hash, old_password):
        flash('Old password is incorrect.')
        return False

    if new_password != confirm_new_password:
        flash('New password does not match confirmation.')
        return False

    update_password_hash = generate_password_hash(new_password)
    update_user_password(update_password_hash)
    return True


def new_login_exists(new_login):
    return False


def get_user_password():
    return 'existing_hashed_password'


def check_password_hash(stored_password_hash, provided_password):
    # Проверка пароля
    return True


def generate_password_hash(password):
    # Генерация хеша пароля
    return 'new_hashed_password'


def update_user_password(new_password_hash):
    # Обновление пароля пользователя
    pass


@app.route('/change_settings', methods=['POST'])
def change_settings():
    new_login = request.form['new_login']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_new_password = request.form['confirm_new_password']

    user = current_user
    updated_login = validate_and_update_login(user.id, new_login)
    updated_password = validate_and_update_password(user, old_password, new_password, confirm_new_password)

    if updated_login and updated_password:
        flash('Настройки успешно обновлены.')
    else:
        flash('Не удалось обновить логин или пароль.')

    return redirect(url_for('personal_page'))


def validate_and_update_login(user_id, new_login):
    if new_login_exists(new_login):
        flash('Этот логин уже используется.')
        return False
    return Database.update_user_login(user_id, new_login)


def validate_and_update_password(user, old_password, new_password, confirm_new_password):
    if not user.check_password(old_password):
        flash('Старый пароль неверен.')
        return False
    if new_password != confirm_new_password:
        flash('Новый пароль не совпадает с подтверждением.')
        return False
    if Database.update_user_password(user.id, new_password):
        return True
    return False
