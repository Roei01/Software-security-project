import pytest
from app import create_app, db as _db
import os, tempfile

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        WTF_CSRF_ENABLED=False,
        SERVER_NAME='localhost.localdomain'
    )
    with app.app_context():
        _db.create_all()
    yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
