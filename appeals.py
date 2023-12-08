from flask import Flask, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://contestormi:RkQc0vo1DmYw@ep-young-haze-43228957.us-east-2.aws.neon.tech/appeals?sslmode=require'
db = SQLAlchemy(app)

class Appeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    house_id = db.Column(db.Integer, nullable=False)
    management_info = db.Column(db.String(255))  # Сохраняем информацию об управляющей организации

@app.route('/appeal', methods=['POST'])
def create_appeal():
    data = request.json
    house_id = data.get('house_id')
    description = data.get('description')

    # Запрос к первому микросервису для получения информации об управляющей организации
    response = requests.get(f'http://house_service:5001/house/{house_id}')
    if response.status_code != 200:
        return jsonify({'error': 'House not found'}), 404

    management_info = response.json()
    new_appeal = Appeal(description=description, house_id=house_id, management_info=str(management_info))
    db.session.add(new_appeal)
    db.session.commit()
    return jsonify({'message': 'Appeal created successfully', 'appeal_id': new_appeal.id}), 201

@app.route('/appeals', methods=['GET'])
def get_appeals():
    appeals = Appeal.query.all()
    appeals_data = [{
        'id': appeal.id,
        'description': appeal.description,
        'house_id': appeal.house_id,
        'management_info': appeal.management_info
    } for appeal in appeals]
    return jsonify(appeals_data), 200

@app.route('/appeal/<int:appeal_id>', methods=['DELETE'])
def delete_appeal(appeal_id):
    appeal_to_delete = Appeal.query.get_or_404(appeal_id)
    db.session.delete(appeal_to_delete)
    db.session.commit()
    return jsonify({'message': 'Appeal deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)
