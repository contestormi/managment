import pytest
from management import app, db, House, Management, Rating

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'

    with app.app_context():
        db.drop_all()
        db.create_all()
        management1 = Management(name="Управляющая Компания 1", contact_info="contact1@example.com")
        db.session.add(management1)
        db.session.commit()

        # Добавление дома
        house1 = House(address="Улица 1, Дом 1", management_id=management1.id)
        db.session.add(house1)
        db.session.commit()

    client = app.test_client()
    yield client


def test_full_application_flow(client):
    rating_data = {"score": 5}
    response = client.post('/rate_management/1', json=rating_data)
    assert response.status_code == 201
  
    response = client.get('/house/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['management_name'] == "Управляющая Компания 1"
    assert data['average_rating'] == 5.0
