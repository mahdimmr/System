from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '68d6b6bf2e38a55c6c7c821e45c57e6d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_POST'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'flask.sup@gmail.com'
app.config['MAIL_PASSWORD'] = 'ZAQ1!qaz'#os.environ.get('MAIL_PASSWORD')
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)
mail = Mail(app)





from Sys import routes