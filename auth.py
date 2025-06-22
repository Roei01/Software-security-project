import os, base64, bcrypt
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from models import db, User
from config import Config
import base64

auth_bp = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ---------- helper: derive key ----------
def _derive_key(password: bytes, salt: bytes) -> Fernet:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=Config.KDF_ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)

# ---------- register ----------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "warning")
            return redirect(url_for(".register"))
        pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        salt = os.urandom(16)
        user = User(username=username, pw_hash=pw_hash, kdf_salt=salt)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for(".login"))
    return render_template("register.html")

# ---------- login ----------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.checkpw(password, user.pw_hash):
            flash("Invalid credentials", "danger")
            return redirect(url_for(".login"))
        login_user(user)
        fernet = _derive_key(password, user.kdf_salt)
        # store key in session (hex) - cleared on logout
        session["fernet_key"] = base64.urlsafe_b64encode(
                fernet._signing_key + fernet._encryption_key
        ).decode()
        return redirect(url_for("vault.dashboard"))
    return render_template("login.html")

# ---------- logout ----------
@auth_bp.route("/logout")
@login_required
def logout():
    session.pop("fernet_key", None)
    logout_user()
    return redirect(url_for(".login"))
