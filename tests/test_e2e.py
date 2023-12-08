import pytest
from appeals import app, db, Appeal
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('ENV_POSTGRES_APPEALS_URL')
    
    with app.app_context():
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.drop_all()

def test_get_appeals(client):
    response = client.get('/appeals')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
