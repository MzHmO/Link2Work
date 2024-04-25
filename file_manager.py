from flask import redirect, send_from_directory, url_for, session, render_template, request
from flask_login import login_required
from werkzeug.utils import secure_filename
from db import Database
import os

def All_app(application):
    global app
    app = application


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
@login_required
def download_file(filename):
    return send_from_directory(str(app.config['UPLOAD_FOLDER'] + "\\" + session['_user_id']), filename,
                               as_attachment=True)

@login_required
def delete_file(filename):
    path = app.config['UPLOAD_FOLDER'] + "\\" + session['_user_id']
    os.remove(os.path.join(path, filename))
    return redirect(url_for('file_handling'))