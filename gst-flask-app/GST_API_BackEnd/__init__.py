from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask import Response, redirect
from werkzeug.exceptions import HTTPException
from flask_admin.contrib.sqla import ModelView
from GST_API_BackEnd.AES import AESCipher

GST_API = Flask("GST_API_BackEnd")
GST_API.config['SECRET_KEY'] = '7ffe2d0fed21d7234581d2dd2a21bb8ab9221fc395e5df81f9382dbaab2c20a7'
GST_API.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
GST_API.config['BASIC_AUTH_USERNAME'] = 'root'
GST_API.config['BASIC_AUTH_PASSWORD'] = 'root'

AES_Key = b"c80825a438f9uird"

Database = SQLAlchemy(GST_API)
Basic_auth = BasicAuth(GST_API)


def GetEncryption(text):
    Text = AESCipher(AES_Key).Encrypt(bytes(str(text).encode('utf-8')))
    Text = (str(Text).replace("'", "")[1:])
    return str(Text)


def GetDecryption(text):
    Text = AESCipher(AES_Key).Decrypt(bytes(text.encode('utf-8')))
    return str(Text)


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}))


class CustomModelView(ModelView):
    def is_accessible(self):
        if not Basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(Basic_auth.challenge())


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not Basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(Basic_auth.challenge())


App_Admin = Admin(GST_API, index_view=CustomAdminIndexView())

from GST_API_BackEnd import LoginSignup_Routs
from GST_API_BackEnd import User_Routs
from GST_API_BackEnd import Process_Routs
from GST_API_BackEnd.models import User, TaxPayer, Tax

App_Admin.add_view(CustomModelView(User, Database.session))
App_Admin.add_view(CustomModelView(TaxPayer, Database.session))
App_Admin.add_view(CustomModelView(Tax, Database.session))

Database.create_all()
Database.session.commit()
