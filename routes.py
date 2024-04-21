from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from db import Database
import os

app = Flask(__name__)
app.secret_key = "l0l1T'sSecretKey!@xD"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'files')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

@app.route('/files', methods=['GET', 'POST'])
@login_required
def file_handling():
    if '_user_id' not in session:
        return redirect(url_for('login'))
    
    user = Database.get_user(session['_user_id'])
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user.id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder, filename))
        return redirect(url_for('file_handling'))

    files = os.listdir(user_folder)
    return render_template('files.html', files=files, username=user.username)

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(str(app.config['UPLOAD_FOLDER'] + "\\" + session['_user_id']), filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['GET', 'POST'])
@login_required
def delete_file(filename):
    path = app.config['UPLOAD_FOLDER'] +  "\\" + session['_user_id']
    os.remove(os.path.join(path, filename))
    return redirect(url_for('file_handling'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def deploy_web(debug, port):
    app.run(debug=debug, port=port)