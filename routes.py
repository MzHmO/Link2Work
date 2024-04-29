from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from db import Database
from file_manager import All_app, download_file, delete_file, file_handling
import os

app = Flask(__name__)
app.secret_key = "l0l1T'sSecretKey!@xD"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'files')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
All_app(app)
app.add_url_rule('/download/<filename>', view_func=download_file)
app.add_url_rule('/delete/<filename>', methods=['GET', 'POST'], view_func=delete_file)
app.add_url_rule('/download/<filename>', view_func=download_file)
app.add_url_rule('/delete/<filename>', methods=['GET', 'POST'], view_func=delete_file)
app.add_url_rule('/files', methods=['GET', 'POST'], view_func=file_handling)


@login_manager.user_loader
def load_user(user_id):
    return Database.get_user(user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('file_handling'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        message, success = Database.register_user(username, password)

        if not success:
            return render_template('register.html', error=message)

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Database.validate_login(username, password):
            user = Database.get_user_by_username(username)
            login_user(user)
            return redirect(url_for('file_handling'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/settings')
def settings():
    render_template('settings.html')

def deploy_web(debug, port):
    app.run(debug=debug, port=port)