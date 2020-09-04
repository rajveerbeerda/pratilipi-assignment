from flask import Flask, render_template, redirect, make_response, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from src.models import AnonymousUser, User

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

migrate = Migrate(app, db)

from src import routes, authy
app.register_blueprint(routes.main_bp)
app.register_blueprint(authy.auth_bp)

db.create_all()
