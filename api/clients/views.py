from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import abort

from api.database import db_session

from api.clients.models import Clients
from api.clients.Schema import client_schema, clients_schema
from api.helpers import response


class ClientsAPI(MethodView):

    def get(self, id):
        if id is None:
            clients = Clients.query.all()
            return clients_schema.jsonify(clients)
        else:
            client = Clients.query.filter(
                Clients.id_ == id).first()

            if not client:
                abort(404)

            return client_schema.jsonify(client)

    def post(self):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        clients = Clients(
            name=data.get('name'),
            address=data.get('address'),
            telephone=data.get('telephone'),
            email=data.get('email')
        )

        db_session.add(clients)
        db_session.commit()

        client = Clients.query.filter(
            Clients.name == data.get('name')).first()

        return client_schema.jsonify(client)

    def delete(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        client = Clients.query.filter(Clients.id_ == id).first()

        if not client:
            abort(404)

        db_session.delete(client)
        db_session.commit()

        return response('success', 'Successfully deleted the item from Client with Id ' + str(id), 200)

    def put(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        client = Clients.query.filter(Clients.id_ == id).first()

        if not client:
            abort(404)

        data = request.get_json()

        client.name = data.get('name'),
        client.address = data.get('address'),
        client.telephone = data.get('telephone'),
        client.email = data.get('email')

        db_session.commit()

        return response('success', 'Successfully updated the item from Clients with Id ' + str(id), 200)
