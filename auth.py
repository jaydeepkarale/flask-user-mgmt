from flask_login import login_user, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from forms import UserRegisterForm, UserLoginForm
from models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    form = UserLoginForm(request.form)
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        username = form.username.data
        password = form.password.data        

        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return render_template('login.html', form=form)

    
        login_user(user)
        return render_template('index.html', user=user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(
            username=form.username.data, 
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='sha256')
            )    

        user = User.query.filter(or_(User.username==form.username.data, User.email==form.email.data)).first() 

        if user:
            flash('Username/Email taken, try with different username.')
            return render_template('register.html', form=form)
        
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template('register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
