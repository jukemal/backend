from flask import jsonify, request, make_response
from flask.views import MethodView
from werkzeug.exceptions import abort
from sqlalchemy import update

from api.database import db_session

from api.bill.models import Bills
from api.bill.Schema import bill_schema, bills_schema

from api.clients.models import Clients

from api.helpers import response


class BillsAPI(MethodView):

    def get(self, id):
        if id is None:
            bills = Bills.query.all()
            return bills_schema.jsonify(bills)
        else:
            bill = Bills.query.filter(Bills.id_ == id).first()

            if not bill:
                abort(404)

            return bill_schema.jsonify(bill)

    def post(self):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        client1 = Clients.query.filter(
            Clients.id_ == data.get('client')).first()

        print(client1.name)

        bill = Bills(
            bill_number=data.get('bill_number'),
            client=client1,
            cashier=data.get('cashier'),
            paid=data.get('paid'),
            date=data.get('date'),
            amount=data.get('amount')
        )

        db_session.add(bill)
        db_session.commit()

        return bill_schema.jsonify(bill)

    def delete(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        bill = Bills.query.filter(Bills.id_ == id).first()

        if not bill:
            abort(404)

        db_session.delete(bill)
        db_session.commit()

        return response('success', 'Successfully deleted the item from Bills with Id ' + str(id), 200)

    def put(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        bill = Bills.query.filter(Bills.id_ == id).first()

        if not bill:
            abort(404)

        data = request.get_json()

        bill.bill_number = data.get('bill_number'),
        bill.cashier = data.get('cashier'),
        # bill.paid = data.get('paid'),
        bill.date = data.get('date'),
        bill.amount = data.get('amount')

        db_session.commit()

        return response('success', 'Successfully updated the item from Bills with Id ' + str(id), 200)
