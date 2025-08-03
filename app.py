from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Пути для загрузки
PENDING_FOLDER = 'static/uploads/pending'
APPROVED_FOLDER = 'static/uploads/approved'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

app.config['UPLOAD_FOLDER'] = PENDING_FOLDER

# Создание папок, если их нет
os.makedirs(PENDING_FOLDER, exist_ok=True)
os.makedirs(APPROVED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(APPROVED_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Нет файла в запросе'
    file = request.files['file']
    if file.filename == '':
        return 'Файл не выбран'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(PENDING_FOLDER, filename))
        return redirect(url_for('index'))
    return 'Недопустимый формат файла'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(APPROVED_FOLDER, filename)

@app.route('/moderate')
def moderate():
    pending_files = os.listdir(PENDING_FOLDER)
    return render_template('moderate.html', files=pending_files)

@app.route('/approve/<filename>')
def approve(filename):
    src = os.path.join(PENDING_FOLDER, filename)
    dst = os.path.join(APPROVED_FOLDER, filename)
    if os.path.exists(src):
        os.rename(src, dst)
    return redirect(url_for('moderate'))

@app.route('/reject/<filename>')
def reject(filename):
    path = os.path.join(PENDING_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for('moderate'))

@app.route('/from-users')
def from_users():
    files = os.listdir(APPROVED_FOLDER)
    return render_template('from_users.html', files=files)

if __name__ == '__main__':
    app.run(debug=True)
