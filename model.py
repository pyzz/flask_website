from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(66))
    email = db.Column(db.String(40))
    #pub_date = db.Column(db.DateTime, default = datetime.datetime.now)
#create_date = db.Column(db.DateTime, default= datetime.datetime.now)

    def __init__(self, username, password, email):
      #  """Initializes the fields with entered data
       # and sets the published date to the current time"""
       self.username = username
       self.password = self._create_password(password)
       self.email = email
       #self.pub_date = pub_date

    def _create_password(self,password):
        return generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password, password)
#return render_template('show_all.html',users=Users.query.order_by(Users.pub_date.desc()).all())
