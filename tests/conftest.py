import pytest
from app import create_app
from app.models import db, init_db, Data, Experiment, Device, Setting, SystemConfig, AppConfig

@pytest.fixture(autouse=True)
def app():
    app = create_app()

    # Assert we are in testing mode
    assert app.config['TESTING'] is True
    assert app.ENV['environment'] == 'testing'

    with app.app_context():
        init_db()
        yield app
        db.close()
        db.drop_tables([Data, Experiment, Device, Setting, SystemConfig, AppConfig], safe=True)

@pytest.fixture
def client(app):
    return app.test_client()
