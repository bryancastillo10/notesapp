from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password= request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You succesffully logged in!', category ='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect passowrd, please try again', category='error')
        else:
            flash('E-mail does not exist. Please sign up first.', category='error')            
    
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('E-mail already exists.', category='error')
        elif len(email) < 4:
            flash('E-mail must be greater than 3 characters. Please try again', category='error')
        elif len(first_name) <2:
            flash('First name must be greater than 1 character. Please try again', category='error')
        elif password1 != password2:
             flash('Passwords don\'t match. Please type again', category='error')
        elif len(password1) < 8:
             flash('Ooopss! Password must be at least 8 characters. Please type again.', category='error')
        else:
            ## Add User to the Database
            new_user = User(email=email,first_name=first_name,password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created! You may now use the APP', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user= current_user)