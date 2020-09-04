from flask import redirect, render_template, flash, Blueprint, request, url_for, session
from flask_login import current_user, login_user, logout_user, login_required

from src import login_manager, app, db
from src.models import User


auth_bp = Blueprint('auth_bp', __name__, template_folder='templates', static_folder='static')


# Flask login

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.', 'warning')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

# Routes

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_anonymous:
        return redirect(url_for('main_bp.dashboard'))
    if request.method=='POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"].lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        existing_user = User.query.filter_by(email=email).first()

        if not existing_user:
            if password!=confirm_password:
                flash("Password doesn't match.", "error")
                return redirect(url_for('auth_bp.register'))

            user = User(first_name=first_name,
                        last_name=last_name,
                        email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash('A user already exists with that email address.', 'error')
            return redirect(url_for('auth_bp.register'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('main_bp.dashboard'))
    if request.method=='POST':
        email = request.form["email"].lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password=password):
            login_user(user)
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash('ERROR! Incorrect login credentials.', 'error')
            return redirect(url_for('auth_bp.login'))
    return render_template('login.html')

