import unittest
from unittest.mock import patch
import json
from appeals import app, db, Appeal  # Импортируйте ваше Flask-приложение и модели

class AppealTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://contestormi:RkQc0vo1DmYw@ep-young-haze-43228957.us-east-2.aws.neon.tech/appeals?sslmode=require'
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('requests.get')  # Мокаем requests.get
    def test_create_appeal(self, mock_get):
        # Мокируем ответ от внешнего сервиса
        mock_get.return_value.json.return_value = {'management_name': 'Test Management'}
        mock_get.return_value.status_code = 200

        response = self.app.post('/appeal', data=json.dumps({
            'house_id': 1,
            'description': 'Test Description'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('Appeal created successfully', str(response.data))

    def test_get_appeals(self):
        response = self.app.get('/appeals')
        self.assertEqual(response.status_code, 200)

    def test_delete_appeal(self):
        # Создаем обращение для удаления
        appeal = Appeal(description='Test', house_id=1, management_info='{}')
        with app.app_context():
            db.session.add(appeal)
            db.session.commit()

            # Перезагружаем объект из базы данных в текущем контексте сессии
            appeal = Appeal.query.get(appeal.id)

            response = self.app.delete(f'/appeal/{appeal.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Appeal deleted successfully', str(response.data))


if __name__ == '__main__':
    unittest.main()
