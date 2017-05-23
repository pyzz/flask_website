# -*- coding: utf-8 -*-
import re
import os
from flask import Flask, request, flash, url_for, redirect, render_template, session, copy_current_request_context
from config import Config
import form
from flask_mail import Mail, Message
from model import db, Users
import threading
# Creates a Flask app and reads the settings from a
# configuration file. We then connect to the database specified
# in the settings file
app = Flask(__name__)
app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Slimshady2.0@localhost/Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail()

def send_email(user_email, username):
  msg = Message('Gracias por tu registro',
                 sender = app.config['MAIL_USERNAME'],
                 recipients = [user_email])
  msg.html = render_template('email.html',username = username)
  mail.send(msg)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.before_request
def before_request():
  if 'username' not in session and request.endpoint in ['loggedin']:
    return redirect(url_for('login')) 
  elif 'username' in session and request.endpoint in ['login']:
    return redirect(url_for('loggedin')) 

@app.route('/', methods=['GET', 'POST'])
def hello_world():
   return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    comment_form = form.RegistrationForm(request.form)
    if request.method == 'POST' and comment_form.validate():
      print comment_form.username.data
      print comment_form.password.data
      print comment_form.email.data
      user = Users(comment_form.username.data,
       comment_form.password.data,
       comment_form.email.data)
      db.session.add(user)
      db.session.commit()
      @copy_current_request_context
      def send_message(email, username):
        send_email(email,username)

      sender = threading.Thread(name ='mail_sender',
                                target = send_message,
                                args = (user.email, user.username))
      sender.start()
      success_message = 'usuario registrado en la base de datos'
      flash(success_message)
      return redirect(url_for('login'))
    elif request.method == 'GET':
      return render_template('index2.html', form = comment_form)

@app.route('/loggedin')
def loggedin():
    """The default route for the app. Displays the list of
    already entered the comments"""
    return render_template('loggedin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = form.RegistrationForm(request.form)
    if request.method == 'POST' :#and login_form.validate():
      username = login_form.username.data
      password = login_form.password.data
      print login_form.password.data
      user = Users.query.filter_by(username = username).first()
      if user is not None and user.verify_password(password):
        success_message = 'bienvenido {}'.format(username)
        flash(success_message)
        session['username'] = username
        return redirect(url_for('loggedin'))
      else:
         error_message = 'usuario pass no validos'
         flash(error_message)
         session['username'] = login_form.username.data
    return render_template('login.html',form = login_form)

@app.route('/logout')
def logout():
  if 'username' in session:
    session.pop('username')
  return redirect(url_for('login'))


# executed.
if __name__ == '__main__':
    # Run the app on all available interfaces on port 80 which is the
    # standard pot for HTTP
    mail.init_app(app)
    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
      db.create_all()

    #port = int(os.environ.get("PORT", 33507))
    #app.run(
     #   host="0.0.0.0",
     #   port=port,

    port = int(os.environ.get("PORT", 5005))
    app.run(
        host="127.0.0.1",
        port=port,
    )


