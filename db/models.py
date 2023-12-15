from . import db
from sqlalchemy.sql import func

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(150), nullable=False)
    dosage = db.Column(db.String(150),nullable=False)
    instructions = db.Column(db.String(250),nullable=False)
    createdAt=db.Column(db.DateTime(timezone=True), default=func.now())
    doctor=db.Column(db.String(150),nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id') )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150),nullable=False)
    last_name = db.Column(db.String(150),nullable=False)
    age = db.Column(db.Integer)
    prescriptions=db.relationship("Prescription")