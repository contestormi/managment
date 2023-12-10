import unittest
from flask_testing import TestCase
from management import app, db, House, Management, Rating
import os

class TestFlaskApp(TestCase):
  
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        management1 = Management(name="Управляющая Компания 1", contact_info="test@example.com")
        db.session.add(management1)
        db.session.commit()
        house1 = House(address="123 Test St", management_id=management1.id)
        db.session.add(house1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    # Test cases
    def test_get_management(self):
        response = self.client.get('/house/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Управляющая Компания 1', response.json['management_name'])

    def test_rate_management_invalid_score(self):
        response = self.client.post('/rate_management/1', json={'score': 6})
        self.assertEqual(response.status_code, 400)

    def test_rate_management_valid_score(self):
        response = self.client.post('/rate_management/1', json={'score': 5})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Rating added successfully', response.json['message'])

if __name__ == '__main__':
    unittest.main()
