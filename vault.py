from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from cryptography.fernet import Fernet
from models import db, PasswordRecord

vault_bp = Blueprint("vault", __name__, url_prefix="/vault")

def _get_fernet():
    key_b64 = session.get("fernet_key")
    if not key_b64:
        flash("Encryption key missing – please log in again.", "danger")
        return None
    return Fernet(key_b64.encode())


@vault_bp.route("/")
@login_required
def dashboard():
    records = PasswordRecord.query.filter_by(user_id=current_user.id).all()
    f = _get_fernet()
    decrypted = [
        {
            "id": r.id,
            "site": r.site,
            "login": r.login,
            "password": f.decrypt(r.enc_password).decode() if f else "***",
        }
        for r in records
    ]
    return render_template("dashboard.html", records=decrypted)

@vault_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_record():
    if request.method == "POST":
        f = _get_fernet()
        assert f
        enc_pw = f.encrypt(request.form["password"].encode())
        rec = PasswordRecord(
            site=request.form["site"],
            login=request.form["login"],
            enc_password=enc_pw,
            owner=current_user,
        )
        db.session.add(rec)
        db.session.commit()
        return redirect(url_for(".dashboard"))
    return render_template("add_edit.html", action="Add")

@vault_bp.route("/edit/<int:rec_id>", methods=["GET", "POST"])
@login_required
def edit_record(rec_id):
    rec = PasswordRecord.query.get_or_404(rec_id)
    f = _get_fernet()
    assert f
    if request.method == "POST":
        rec.site = request.form["site"]
        rec.login = request.form["login"]
        rec.enc_password = f.encrypt(request.form["password"].encode())
        db.session.commit()
        return redirect(url_for(".dashboard"))
    record = {
        "site": rec.site,
        "login": rec.login,
        "password": f.decrypt(rec.enc_password).decode(),
    }
    return render_template("add_edit.html", action="Edit", record=record, rec_id=rec_id)

@vault_bp.route("/delete/<int:rec_id>", methods=["POST"])
@login_required
def delete_record(rec_id):
    PasswordRecord.query.filter_by(id=rec_id, user_id=current_user.id).delete()
    db.session.commit()
    return redirect(url_for(".dashboard"))
