from flask import render_template,redirect,url_for,Blueprint
from flask_login import login_required, current_user
from datetime import datetime
from .models.database import session
from .models.picture import Picture
from .models.folder import Folder

main = Blueprint("main", __name__, template_folder='templates')

@main.route("/")
def index():
    folder = session.query(Folder).filter_by(id='1').first()
    pictures = ''
    if folder:
        pictures = session.query(Picture).filter_by(folder=folder.name).all()
    return render_template('index.html', pictures=pictures)

@main.route("/about")
def about():
    return render_template('about.html')

@main.route("/project")
def projects():
    folders = session.query(Folder).all()
    if folders is None:
        folders = ''
    return render_template('projects.html', folders=folders)

@main.route("/project/<folder_name>/", methods=['GET','POST'])
def project(folder_name):
    folder = session.query(Folder).filter_by(name=folder_name).first()
    pictures = ''
    if session.query(Picture).filter_by(folder=folder_name).first() is not None:
        pictures = session.query(Picture).filter_by(folder=folder_name)
    
    return render_template('project.html', pictures=pictures, folder_name=folder_name, commentary=folder.commentary, project_date=folder.created_at.strftime("%B %d, %Y"))

    
