from flask import Flask
from config import Config
from models import db
from auth import auth_bp, login_manager
from vault import vault_bp
import webbrowser
import threading
import time

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
        return "Welcome to Secure Password Manager"

    return app

if __name__ == "__main__":
    app = create_app()
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("https://localhost:4000/login", new=2)
    threading.Thread(target=open_browser).start()

    # Run with valid local certificate
    app.run(
        host="0.0.0.0",
        port=4000,
        ssl_context=("localhost+2.pem", "localhost+2-key.pem")
    )

