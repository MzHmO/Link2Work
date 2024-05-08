from flask import Flask
import os

app = Flask(__name__, template_folder=os.getcwd() + '\\templates', static_folder=os.getcwd() + '\\static')
app.secret_key = "l0l1T'sSecretKey!@xD"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'files')