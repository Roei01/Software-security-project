import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SPM_SECRET') or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'vault.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # PBKDF2 iterations for deriving encryption key
    KDF_ITERATIONS = 260_000
