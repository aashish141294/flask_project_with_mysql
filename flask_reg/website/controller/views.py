from flask import Blueprint, render_template, request, flash,redirect,url_for,g,session
from website import db
from website.models import Users
from website.routes import views
import os
from website import create_app
import urllib.request
from werkzeug.utils import secure_filename

folder = create_app().config['UPLOAD_FOLDER']
@views.route('/home', methods=['GET', 'POST'])
def home():
  if g.user:
    all_user = Users.query.all()
    return render_template("home.html",all_user=all_user,user=session['user'])
  return render_template("login.html")

@views.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
  if g.user:  
    user = Users.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('views.home'))
  return render_template("login.html")

@views.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
  if g.user:  
    if request.method == 'POST':
      first_name = request.form['first_name']
      email = request.form['email']  
      password1 = request.form['password1']
      password2 = request.form['password1']
      gender = request.form.get('gender')
      country = request.form.get('country')
      state = request.form.get('state')
      city = request.form.get('city')
      zip = request.form.get('zip')
      checkbox = request.form.getlist('check')
      file = request.files['file']
      filename = secure_filename(file.filename)
      if 'file' in request.files:
        file.save(os.path.join(folder, filename))
        
      user = Users.query.filter_by(id=id).first()
      user.first_name = first_name
      user.email = email
      user.gender = gender
      user.country = country
      user.state = state
      user.city = city
      user.zip = zip
      user.area_of_intrest = ','.join(checkbox)
      user.file_name = filename
      user.password = password1
      if password1 != password2:
        flash('Passwords don\'t match.', category='error')
      else:
        db.session.add(user)
        db.session.commit()
        flash('User Updated!', category='success')
        return render_template('update.html',user=user)
    user = Users.query.filter_by(id=id).first()
    checkbox_data = user.area_of_intrest.split(",")          
    return render_template('update.html',user = user,checkbox_data = checkbox_data)
  return render_template("login.html")


# middelware
@views.before_request
def before_request():
  g.user = None
  if 'user' in session:
    g.user = session['user']