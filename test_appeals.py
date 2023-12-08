import unittest
from flask_testing import TestCase
import json
from unittest.mock import patch
from appeals import app, db, Appeal

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestAppealService(BaseTestCase):

    @patch('requests.get')  # Mock the requests.get call
    def test_create_appeal(self, mock_get):
        # Mock response for the external service
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'management_info': 'Test Info'}

        response = self.client.post('/appeal', data=json.dumps({
            'house_id': 1,
            'description': 'Leaky faucet'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('Appeal created successfully', response.data.decode())

    def test_get_appeals(self):
        # Add a test appeal
        test_appeal = Appeal(description="Broken window", house_id=2, management_info="Info")
        db.session.add(test_appeal)
        db.session.commit()

        response = self.client.get('/appeals')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Broken window', response.data.decode())

    def test_delete_appeal(self):
        # Add a test appeal
        test_appeal = Appeal(description="Noise complaint", house_id=3, management_info="Info")
        db.session.add(test_appeal)
        db.session.commit()

        response = self.client.delete(f'/appeal/{test_appeal.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Appeal deleted successfully', response.data.decode())

if __name__ == '__main__':
    unittest.main()
