# app.py
from flask import Flask, redirect, url_for 
from flask_login import current_user         
from config import Config
from models import db
from auth import auth_bp, login_manager
from vault import vault_bp
import webbrowser, threading, time
import werkzeug.serving as ws


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(vault_bp)

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    @app.errorhandler(404)
    def handle_404(e):
        if current_user.is_authenticated:
            return redirect(url_for("vault.dashboard"))
        return redirect(url_for("auth.login"))

    return app


if __name__ == "__main__":
    app = create_app()

    def open_browser():
        time.sleep(1.5)
        webbrowser.open("https://localhost:4000/login", new=2)
    threading.Thread(target=open_browser, daemon=True).start()


    _orig_log = ws._log
    def _log(type, message, *args):
        if type == "info" and "Running on https://" in message:
            message = message.replace("https://127.0.0.1", "https://localhost")
        return _orig_log(type, message, *args)

    ws._log = _log

    # Run with valid local certificate
    app.run(
        host="0.0.0.0",
        port=4000,
        ssl_context=("localhost+2.pem", "localhost+2-key.pem"),
    )
