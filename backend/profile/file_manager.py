import os
import uuid
from flask import redirect, send_from_directory, url_for, session, render_template, request
from flask_login import login_required
from werkzeug.utils import secure_filename
from backend.database import Database
from config import app


files_mapping = {}

@login_required
def file_handling():
    try:
        if '_user_id' not in session:
            return redirect(url_for('login'))

        user = Database.get_user_by_id(session['_user_id'])
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user.id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                extension = filename.split('.')[-1].lower()
                allowed_extensions = ["png", "jpg", "jpeg", "txt", "mkv"]
                if extension in allowed_extensions:
                    if len(filename) > 15:
                        filename = filename[:15] + '.' + extension

                    guid = str(uuid.uuid4())
                    filename_with_guid = f"{guid}.{extension}"

                    files_mapping[filename_with_guid] = filename

                    path = os.path.join(user_folder, filename_with_guid)

                    file.save(path)
                    size = round(os.path.getsize(path) / 1024 ** 2, 2)
                    if size > 100:
                        os.remove(path)
                        files = [f for f in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, f))]
                        return render_template('files.html', files=files, username=user.username, error="Файл не должен превышать 100MB.")
                    return redirect(url_for('file_handling'))
                else:
                    error_message = "Допускаются только файлы с расширениями: " + ', '.join(allowed_extensions) + "."
                    files = [f for f in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, f))]
                    return render_template('files.html', files=files, username=user.username, error=error_message)
            else:
                error_message = "Вы не загрузили файл"
                files = [f for f in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, f))]
                return render_template('files.html', files=files, username=user.username, error=error_message)
        
        elif request.method == 'GET':
            files = [files_mapping.get(f) for f in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, f))]
            return render_template('files.html', files=files, username=user.username)
    except Exception as e:
        files = [files_mapping.get(f.split(".")[0]) for f in os.listdir(user_folder) if
                 os.path.isfile(os.path.join(user_folder, f))]
        return render_template('files.html', files=files, username=user.username, error=str(e))


        
@login_required
def download_file(filename):
    key_for_download = None
    for key, value in files_mapping.items():
        if value == filename:
            key_for_download = key
    if key_for_download is not None:
        return send_from_directory(str(app.config['UPLOAD_FOLDER'] + "\\" + session['_user_id']), key_for_download, as_attachment=True)

@login_required
def delete_file(filename):
    path = app.config['UPLOAD_FOLDER'] + "\\" + session['_user_id']
    key_for_delete = None
    for key, value in files_mapping.items():
        if value == filename:
            key_for_delete = key
    if key_for_delete is not None:
        del files_mapping[key_for_delete]
        os.remove(os.path.join(path, key_for_delete))
    return redirect(url_for('file_handling'))