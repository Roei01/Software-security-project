from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pw_hash = db.Column(db.LargeBinary(60), nullable=False)   # bcrypt hash
    kdf_salt = db.Column(db.LargeBinary(16), nullable=False)  # PBKDF2 salt
    records = db.relationship("PasswordRecord", backref="owner", lazy=True)

class PasswordRecord(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(120), nullable=False)
    login = db.Column(db.String(120), nullable=False)
    enc_password = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
