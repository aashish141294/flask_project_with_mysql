from flask import Blueprint, render_template, request, flash, redirect, url_for,g,session
from website.models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from website import db 
from website.routes import auth
import os
from website import create_app
import urllib.request


folder = create_app().config['UPLOAD_FOLDER']
@auth.route('/login', methods=['GET', 'POST'])
def login():
    print('---->',create_app().config['UPLOAD_FOLDER'])
    if request.method == 'POST':
        session.pop('user',None)
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                session['user'] = request.form['email']
                print('----->',session['user'])
                all_user = Users.query.all()
                return render_template("home.html",all_user=all_user,session=session['user'])
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html",session = None)


@auth.route('/logout')
def logout():
    session.pop('user',None)
    return render_template("login.html",session = None)


@auth.route('/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        gender = request.form.get('gender')
        country = request.form.get('country')
        state = request.form.get('state')
        city = request.form.get('city')
        zip = request.form.get('zip')
        checkbox = request.form.getlist('check')
        file = request.files['file']
        filename = secure_filename(file.filename)
        print('----->',file,filename)
        file.save(os.path.join(create_app().config['UPLOAD_FOLDER'], filename))
                    
        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Users(first_name=first_name,last_name=last_name,email=email, password=generate_password_hash(
                password1, method='sha256'),gender=gender,country=country,state=state,city=city,zip=zip,area_of_intrest=','.join(checkbox),file_name = filename)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return render_template("sign_up.html",session = None)
    return render_template("sign_up.html",session = None)
