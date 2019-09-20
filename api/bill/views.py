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
    """
        class for "/bills/" endpoint
    """

    def get(self, id):
        """function for "GET /bills/" endpoint

        Args:
            id (int): id for the Bill

        Returns:
            If endpoint is "GET /bills/<id>"
                {
                    "amount": 10000,
                    "bill_number": "100",
                    "cashier": "Cashier 1",
                    "client": 1,
                    "client_name": "Client 1",
                    "created_at": "2019-09-20T06:07:23.789286",
                    "date": "2019-10-15T00:00:00",
                    "id_": 1,
                    "paid": false,
                    "updated_at": null
                }

            If endpoint is "GET /bills/"
                [
                    {
                        "amount": 10000,
                        "bill_number": "100",
                        "cashier": "Cashier 1",
                        "client": 1,
                        "client_name": "Client 1",
                        "created_at": "2019-09-20T06:07:23.789286",
                        "date": "2019-10-15T00:00:00",
                        "id_": 1,
                        "paid": false,
                        "updated_at": null
                    },
                    {
                        "amount": 10000,
                        "bill_number": "101",
                        "cashier": "Cashier 1",
                        "client": 3,
                        "client_name": "Client 3",
                        "created_at": "2019-09-20T06:07:23.792931",
                        "date": "2019-10-15T00:00:00",
                        "id_": 2,
                        "paid": false,
                        "updated_at": null
                    }
                ]
        """

        if id is None:
            bills = Bills.query.all()
            return bills_schema.jsonify(bills)
        else:
            bill = Bills.query.filter(Bills.id_ == id).first()

            if not bill:
                abort(404)

            return bill_schema.jsonify(bill)

    def post(self):
        """function for "POST /bills/" endpoint

        Returns:
            {
                "amount": 10000,
                "bill_number": "100",
                "cashier": "Cashier 1",
                "client": 1,
                "client_name": "Client 1",
                "created_at": "2019-09-20T06:07:23.789286",
                "date": "2019-10-15T00:00:00",
                "id_": 1,
                "paid": false,
                "updated_at": null
            }
        """

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
        """function for "DELETE /bills/<id>" endpoint

        Args:
            id (int): id for the Client

        Returns:
            {
                "status" : "success,
                "message" : "Successfully deleted the item from Bills with Id 1"
            }
        """

        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        bill = Bills.query.filter(Bills.id_ == id).first()

        if not bill:
            abort(404)

        db_session.delete(bill)
        db_session.commit()

        return response('success', 'Successfully deleted the item from Bills with Id ' + str(id), 200)

    def put(self, id):
        """function for "PUT /bills/<id>" endpoint

        Args:
            id (int): id for the Client

        Returns:
            {
                "status" : "success,
                "message" : "Successfully updated the item from Bills with Id 1"
            }
        """

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
