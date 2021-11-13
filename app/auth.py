import flask
from flask import Flask,render_template,redirect,url_for,request,Blueprint,flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from .models.database import session
from .models.user import User
from .form import LoginForm

#Blueprint as Main
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash('*ログイン情報に誤りがあります。', 'error')
            return redirect(url_for('auth.login')) 

        login_user(user)
        flask.session.permanent = True

        return redirect(url_for('admin.home'))

    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

