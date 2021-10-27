from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register')
def show_register_page():
    return render_template('register.html')


@auth.route('/login')
def show_login_page():
    return render_template('login.html')


@auth.route('/reset_password')
def show_reset_password_page():
    pass
