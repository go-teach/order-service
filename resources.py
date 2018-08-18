import requests
from flask import jsonify, request
from flask_restful import Resource, reqparse
from models import OrderModel
from constants import COST_PER_HOUR


class OrderIndex(Resource):
    def get(self):
        query = OrderModel.query
        student = request.form.get('student', None)
        subject = request.form.get('subject', None)
        
        if student:
            query = query.filter_by(student = student)
        if subject:
            query = query.filter_by(subject = subject)
        return jsonify({"orders": [order.serialize() for order in query.all()]})

    def post(self):
        student = request.form['student']
        subject = request.form['subject']
        address = request.form['address']
        duration = int(request.form['duration'])
        payment_type = request.form['payment_type']

        balance = requests.get('http://go-teach-balance.herokuapp.com/balances/{}'.format(student)).json()
        total_cost = COST_PER_HOUR*duration
        if balance['amount'] >= total_cost or payment_type == 'cash':
            order = OrderModel(student = student,
                               teacher = '',
                               subject = subject,
                               address = address, 
                               duration = duration,
                               payment_type = payment_type,
                               status = 'available')
            if payment_type != 'cash':
                requests.post('http://go-teach-balance.herokuapp.com/balances/{}/charge',
                              data = {'amount': total_cost})
            order.save_to_db()
            return {'status': 'OK'}
        else:
            return {'status': 'Balance not enough'}


class OrderDetail(Resource):
    def get(self, order_id):
        order = OrderModel.query.filter_by(id = order_id).first()
        if order:
            return jsonify(order.serialize())
        else:
            return {'status': 'Not Found'}, 404

    def put(self, order_id):
        order = OrderModel.query.filter_by(id = order_id).first()
        action = request.form['action']
        if action:
            if  action == 'take':
                order.status = 'taken'
                order.teacher = request.form['teacher']
            elif action == 'cancel':
                order.status = 'cancelled'
            order.save_to_db()
            return {'status': 'OK'}
        else:
            return {'status': 'Bad Request'}, 400
