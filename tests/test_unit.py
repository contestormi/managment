import unittest
from unittest.mock import patch
from flask import json
from appeals import app, db, Appeal
import os

class AppealTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('ENV_POSTGRES_APPEALS_URL')
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('requests.get')
    def test_create_appeal(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'management_name': 'Test Management'}

        response = self.app.post('/appeal', data=json.dumps({
            'house_id': 1,
            'description': 'Test Description'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Appeal created successfully')

    def test_get_appeals(self):
        # Добавляем тестовые данные
        test_appeal = Appeal(description='Test', house_id=1, management_info='Test Management Info')
        with app.app_context():
            db.session.add(test_appeal)
            db.session.commit()

        response = self.app.get('/appeals')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['description'], 'Test')

    def test_delete_appeal(self):
        # Добавляем тестовые данные
        test_appeal = Appeal(description='Test', house_id=1, management_info='Test Management Info')
        with app.app_context():
            db.session.add(test_appeal)
            db.session.flush()

            test_appeal = Appeal.query.get(test_appeal.id)

            response = self.app.delete(f'/appeal/{test_appeal.id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Appeal deleted successfully')


if __name__ == '__main__':
    unittest.main()
