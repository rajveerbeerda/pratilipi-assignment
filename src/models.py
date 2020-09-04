from . import db
from sqlalchemy import ForeignKey
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class ValidationError(ValueError):
    pass

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False, unique=False)
    last_name = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def is_active(self):
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class AnonymousUser(AnonymousUserMixin):
    @property
    def id(self):
        return None

    @property
    def is_admin(self):
        return None

    def get_user(self):
        return None

class Stories(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    author = db.Column(db.String(100), nullable=False, unique=False)
    category = db.Column(db.String(100), nullable=False, unique=False)
    seen_by = db.Column(db.Integer, unique=False, nullable=False)
    story_path = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    live_users = db.Column(db.Integer, unique=False, nullable=False)
