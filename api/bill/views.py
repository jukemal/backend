from flask import jsonify, request, make_response
from flask.views import MethodView
from werkzeug.exceptions import abort
from sqlalchemy import func

from api.database import db_session

from api.bill.models import Bills
from api.bill.Schema import bill_schema, bills_schema

from api.clients.models import Clients

from api.helpers import response


class BillsAPI(MethodView):
    def get(self, id):
        if id is None:
            bills = Bills.query.all()

            report = Bills.query.with_entities(func.date_trunc("day", Bills.date).label("date"), func.count(
                Bills.bill_number).label("count")).group_by(func.date_trunc("day", Bills.date)).all()

            return jsonify(data=bills_schema.dump(bills), report=report)

            return bills_schema.jsonify(bills)
        else:
            bill = Bills.query.filter(Bills.id_ == id).first()

            if not bill:
                return response('Not Found', f'Bill with Bill Code {id} is not available.', 404)

            return bill_schema.jsonify(bill)

    def post(self):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        fields = ['client', 'cashier', 'paid','date', 'amount']
        string = ''

        for i in fields:
            if not data.get(f'{i}'):
                string = string+f'\"{i}\", '

        isPaid=False

        if data.get('paid')=="paid":
            isPaid=True

        if string:
            return response('Invalid POST Request', f'These fields should be included in the POST Request. {string}', 404)

        client1 = Clients.query.filter(Clients.id_ == data.get('client')).first()

        bill = Bills(
            bill_number="100",
            client=client1,
            cashier=data.get('cashier'),
            paid=isPaid,
            date=data.get('date'),
            amount=data.get('amount')
        )

        db_session.add(bill)
        db_session.commit()

        return response('Added Successfully.', f'Successfully added the Bill with Code {str(bill.bill_number)}', 200, bill_schema.dump(bill))

    def delete(self, id):
        bill = Bills.query.filter(Bills.id_ == id).first()

        if not bill:
            return response('Not Found', f'Bill with Bill Code {id} is not available.', 404)

        db_session.delete(bill)
        db_session.commit()

        return response('Deleted Successfully.', f'Successfully deleted the Bill with Code {str(bill.bill_number)}', 200, bill_schema.dump(bill))

    def put(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        bill = Bills.query.filter(Bills.id_ == id).first()

        if not bill:
            return response('Not Found', f'Bill with Bill Code {id} is not available.', 404)

        data = request.get_json()

        print(data)

        # if data.get('bill_number'):
        #     bill.bill_number = data.get('bill_number')

        if data.get('client'):
            bill.client_id = data.get('client')

        if data.get('cashier'):
            bill.cashier = data.get('cashier')

        if data.get('paid') == "paid":
            bill.paid = True
        else:
            bill.paid = False

        if data.get('date'):
            bill.date = data.get('date')

        if data.get('amount'):
            bill.amount = data.get('amount')

        db_session.commit()

        return response('Updated Successfully.', f'Successfully updated the Bill with Code {str(bill.bill_number)}', 200, bill_schema.dump(bill))
