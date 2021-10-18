from flask import render_template,redirect,url_for,Blueprint,request,flash
from flask_login import login_required, current_user
from .form import PictureUploadForm, NewFolderForm, CommentaryEditForm

from werkzeug.utils import secure_filename

from .models.database import session
from .models.picture import Picture
from .models.folder import Folder

from datetime import datetime
import shutil

import os

admin = Blueprint("admin", __name__, template_folder='templates')

@admin.route("/admin")
@login_required
def home():
    picture = session.query(Picture).order_by(Picture.id.desc()).first()
    return render_template('admin/admin.html', picture=picture)

@admin.route("/admin/picture/", methods=['GET','POST'])
@login_required
def picture():
    folders = session.query(Folder).all()

    if request.method == 'POST':
        selected_folders = request.form.getlist("selected")

        for selected_folder in selected_folders:
            found_folder = Folder.query.filter_by(id=selected_folder).first()
            folder_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), './static/images', found_folder.name)
            shutil.rmtree(folder_path)

            #Delete Pictures in Deleted Folder
            pictures_in_folder = session.query(Picture).filter_by(folder=found_folder.name).all()
            for picture_in_folder in pictures_in_folder:
                session.delete(picture_in_folder)
                session.commit()

            session.delete(found_folder)
            session.commit()
        flash('*フォルダーの削除が完了しました。')
        return redirect(url_for('admin.picture'))

    return render_template('admin/picture/picture.html', folders=folders)

@admin.route("/admin/picture/folder/<folder_name>/", methods=['GET','POST'])
@login_required
def folder(folder_name):
    pictures = session.query(Picture).filter_by(folder=folder_name)

    if request.method == 'POST':
        selected_pictures = request.form.getlist("selected")

        for selected_picture in selected_pictures:
            found_picture = Picture.query.filter_by(id=selected_picture).first()
            basedir = os.path.abspath(os.path.dirname(__file__))
            os.remove(os.path.join(basedir, './static/images', folder_name, found_picture.picture_url))
            session.delete(found_picture)
            session.commit()
        flash('*写真の削除が完了しました。')
        new_pictures = session.query(Picture).filter_by(folder=folder_name)
        return redirect(url_for('admin.folder', folder_name=folder_name, pictures=new_pictures))

    return render_template('admin/picture/folder.html', pictures=pictures, folder_name=folder_name)

@admin.route("/admin/picture/create_folder/", methods=['GET','POST'])
@login_required
def create_folder():
    form = NewFolderForm(request.form)

    if request.method == 'POST' and form.validate():
        folders = [x.strip() for x in form.folder.data.split(',')]
        commentary = form.commentary.data

        for folder in folders:

            same_folder = Folder.query.filter_by(name=folder).first()
            if same_folder:
                flash('*同じ名前のフォルダーが既に存在します。', 'error')
                return redirect(url_for('admin.create_folder')) # if the user doesn't exist or password is wrong, reload the page
            
            folder_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), './static/images', folder)
            os.mkdir(folder_path)
            new_folder = Folder(name=folder, commentary=commentary, created_at=datetime.now()) 
            session.add(new_folder)
            session.commit()

        flash('*フォルダー作成が完了しました。')
        return redirect(url_for('admin.picture'))


    return render_template('admin/picture/new_folder.html', form=form)


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
def allowed_file(filename, form, folder_name):
    path, ext = os.path.splitext(filename)
    #if ext not in ALLOWED_EXTENSIONS:
        #return flash('*' + ext + '拡張子がサポートされていません。')
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@admin.route("/admin/picture/folder/<folder_name>/upload/", methods=['GET','POST'])
@login_required
def upload(folder_name):
    form = PictureUploadForm(request.form)

    if request.method == 'POST':
        pictures = request.files.getlist(form.pictures.name)
        for picture in pictures:
            if allowed_file(picture.filename, form, folder_name):
                picture_url = secure_filename(picture.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                picture.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), './static/images/', folder_name, picture_url))
                new_upload = Picture(picture_url=picture_url, folder=folder_name, uploaded_at=datetime.now())
                session.add(new_upload)
                session.commit()
                flash('*アップロードが完了しました。')
        
        new_pictures = session.query(Picture).filter_by(folder=folder_name)
        return redirect(url_for('admin.folder', folder_name=folder_name, pictures=new_pictures))
        
        
    return render_template('admin/picture/upload.html', form=form, folder_name=folder_name)


@admin.route("/admin/picture/folder/<folder_name>/edit/", methods=['GET','POST'])
@login_required
def edit(folder_name):
    form = CommentaryEditForm(request.form)

    folder = session.query(Folder).filter_by(name=folder_name).first()

    if request.method == 'GET':
        form.commentary.data = folder.commentary

    if request.method == 'POST':
        new_commentary = form.commentary.data
        folder.commentary = new_commentary
        session.commit()
        flash('*解説の編集が完了しました。')
        return redirect(url_for('admin.folder', folder_name=folder_name))

    return render_template('admin/picture/edit.html', form=form, folder_name=folder_name)
