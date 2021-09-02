from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os, flask

cwd = os.getcwd()
upload_folder = os.path.join(cwd,'public')

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = upload_folder

@app.route('/status')
def status():
    return("The Public Server for plugin testing is up and running")

@app.route('/upload')
def upload_file_template():
   return render_template('upload.html')

@app.route('/file_list')
def file_list():
    f_list = os.listdir(upload_folder)
    return render_template('file_list.html', f_list = f_list)
	
@app.route('/uploader', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(upload_folder, secure_filename(f.filename)))
      return render_template('upload_success.html', file_uploaded=secure_filename(f.filename))

@app.route('/delete/<file_name>')
def delete(file_name):
    try:
        os.remove(os.path.join(upload_folder, secure_filename(file_name)))
        return render_template('file_deleted.html', file_name=secure_filename(file_name))
    except:
        return render_template('Static_File_Not_Found.html', file_name=secure_filename(file_name)), 404


@app.route('/download/<file_name>')
def download(file_name):
    try:
        return flask.send_from_directory(upload_folder, secure_filename(file_name))
    except:
        return render_template('Static_File_Not_Found.html', file_name=secure_filename(file_name)), 404