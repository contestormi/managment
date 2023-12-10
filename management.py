from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('ENV_POSTGRES_MANAGMENT_URL')
db = SQLAlchemy(app)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), unique=True, nullable=False)
    management_id = db.Column(db.Integer, db.ForeignKey('management.id'), nullable=False)

class Management(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    contact_info = db.Column(db.String(120))
    ratings = db.relationship('Rating', backref='management', lazy=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    management_id = db.Column(db.Integer, db.ForeignKey('management.id'), nullable=False)

@app.route('/house/<int:house_id>')
def get_management(house_id):
    house = House.query.get_or_404(house_id)
    management = Management.query.get_or_404(house.management_id)
    average_rating = None
    if management.ratings:
        average_rating = sum(rating.score for rating in management.ratings) / len(management.ratings)
    return jsonify({
        'management_name': management.name,
        'contact_info': management.contact_info,
        'average_rating': average_rating
    })

@app.route('/rate_management/<int:management_id>', methods=['POST'])
def rate_management(management_id):
    score = request.json.get('score')
    if not score or not (1 <= score <= 5):
        return jsonify({'error': 'Invalid score'}), 400
    rating = Rating(score=score, management_id=management_id)
    db.session.add(rating)
    db.session.commit()
    return jsonify({'message': 'Rating added successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Management.query.first():
            # Добавление данных управляющей организации
            management1 = Management(name="Управляющая Компания 1", contact_info="contact1@example.com")
            db.session.add(management1)
            db.session.commit()

            # Добавление дома
            house1 = House(address="Улица 1, Дом 1", management_id=management1.id)
            db.session.add(house1)
            db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=os.environ['PORT'])
