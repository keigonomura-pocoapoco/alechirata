from flask import render_template,redirect,url_for,Blueprint
from flask_login import login_required, current_user
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

    
