#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    result = []
    for bakery in bakeries:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'updated_at': bakery.updated_at,
            'baked_goods': [baked_good.serialize() for baked_good in bakery.baked_goods]
        }
        result.append(bakery_data)
    return jsonify(result)

# Define route to get bakery by ID
@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.serialize())

# Define route to get baked goods sorted by price in descending order
@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([baked_good.serialize() for baked_good in baked_goods])

# Define route to get the most expensive baked good
@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(most_expensive_baked_good.serialize())


if __name__ == '__main__':
    app.run(port=5555, debug=True)
