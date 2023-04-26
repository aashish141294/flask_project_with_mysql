from . import db
from sqlalchemy.sql import func
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(10))
    last_name = db.Column(db.String(10))
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))
    gender = db.Column(db.String(10))
    country = db.Column(db.String(20))
    state = db.Column(db.String(20))
    city = db.Column(db.String(20))
    zip = db.Column(db.Integer)
    area_of_intrest = db.Column(db.String(50))
    file_name = db.Column(db.String(50),default='')
    date_created = db.Column(db.DateTime,default = datetime.utcnow)
 
    def __repr__(self) -> str:
        return f"{self.id} - {self.first_name}  - {self.email} - {self.password} - {self.area_of_intrest}"
