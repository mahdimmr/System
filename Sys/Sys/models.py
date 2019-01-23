from Sys import db, login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), nullable=False, unique=True)
    email = db.Column('email', db.String(120), nullable=False, unique=True)
    password = db.Column('password', db.String(60), nullable=False)
    image_file = db.Column('image_file', db.String)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}'"

