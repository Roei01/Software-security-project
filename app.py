from flask import Flask
from config import Config
from models import db
from auth import auth_bp, login_manager
from vault import vault_bp

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
    # Run with adhoc SSL for local HTTPS
    app.run(host="0.0.0.0", port=4000, ssl_context="adhoc")

