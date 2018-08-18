import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", default="sqlite:///app.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", default='set-the-secret-key-in-env-please')

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

import models, resources

api.add_resource(resources.OrderIndex, '/orders')
api.add_resource(resources.OrderDetail, '/orders/<int:order_id>')
