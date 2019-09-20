import os

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_marshmallow import Marshmallow
from api.database import Base
from flask_migrate import Migrate
from flask_cors import CORS

from api.config import DATA_SOURCE

ma = Marshmallow()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=DATA_SOURCE,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    
    CORS(app)

    ma.init_app(app)

    migrate = Migrate(app, Base)

    def register_api(view, endpoint, url, pk='id', pk_type='int'):
        view_func = view.as_view(endpoint)
        app.add_url_rule(url, defaults={pk: None},
                         view_func=view_func, methods=['GET', ])
        app.add_url_rule(url, view_func=view_func, methods=['POST', ])
        app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                         methods=['GET', 'PUT', 'DELETE'])

    from api.items import ItemsAPI
    from api.distributors import DistributorsAPI
    from api.clients import ClientsAPI
    from api.payments import PaymentsAPI
    from api.bill import BillsAPI

    register_api(ItemsAPI, 'items_api', '/items/', pk='item_code')
    register_api(DistributorsAPI, 'distributor_api',
                 '/distributors/', pk='id')
    register_api(ClientsAPI, 'clients_api', '/clients/', pk='id')
    register_api(PaymentsAPI, 'payments_api', '/payments/', pk='id')
    register_api(BillsAPI, 'bills_api', '/bills/', pk='id')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from api.database import db_session
        db_session.remove()

    return app
