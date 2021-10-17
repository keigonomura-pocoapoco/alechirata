from wtforms import Form, BooleanField, StringField, FileField, TextAreaField, PasswordField, MultipleFileField, validators, ValidationError
from werkzeug.utils import secure_filename
from flask import flash, redirect, url_for
from .models.user import User
from .models.folder import Folder

class LoginForm(Form):
    email = StringField('メールアドレス', [validators.Length(min=6, max=35, message="*6文字以上35文字以内で入力してください"), validators.DataRequired(message="*メールアドレスを入力してください")], render_kw={"placeholder": "メールアドレス"})
    password = PasswordField('パスワード', [
        validators.Length(min=4, max=25, message="*4文字以上25文字以内で入力してください"),
        validators.DataRequired(message="*パスワードを入力してください")],
        render_kw={"placeholder": "パスワード"}
    )
    remember = BooleanField('Remember me')

    def validate_login(self, email, password):
        user = User.query.filter_by(email=email.data).first()
        if not user or not check_password_hash(user.password, password.data):
            flash('*ログイン情報に誤りがあります。', 'error')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

class PictureUploadForm(Form):
    pictures = MultipleFileField('File(s) Upload')

class NewFolderForm(Form):
    folder = StringField('フォルダー名', [validators.Length(min=3, message="*3文字以上で入力してください"), validators.DataRequired(message="*フォルダー名を入力してください")], render_kw={"placeholder": "フォルダー"})
    commentary = TextAreaField('解説', [validators.Length(min=3, message="*3文字以上で入力してください"), validators.DataRequired(message="*解説を入力してください")], render_kw={"placeholder": "解説 / Commentary"})
    def validate_folder(self, folder):
        folder = Folder.query.filter_by(name=folder.data).first()
        if folder:
            flash('*同じ名前のフォルダーが存在します。', 'error')
            return redirect(url_for('admin.create_folder')) # if the user doesn't exist or password is wrong, reload the page

class CommentaryEditForm(Form):
    commentary = TextAreaField('解説', [validators.Length(min=3, message="*3文字以上で入力してください"), validators.DataRequired(message="*解説を入力してください")], render_kw={"placeholder": "解説 / Commentary"})
    
    




    