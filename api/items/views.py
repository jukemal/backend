from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import abort

from api.database import db_session

from api.items.models import Items
from api.items.Schema import item_schema, items_schema

from api.helpers import response


class ItemsAPI(MethodView):

    def get(self, item_code):
        if item_code is None:
            items = Items.query.all()
            return items_schema.jsonify(items)
        else:
            item = Items.query.filter(Items.item_code == item_code).first()

            if not item:
                abort(404)

            return item_schema.jsonify(item)

    def post(self):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        item = Items(
            item_code=data.get('item_code'),
            name=data.get('name'),
            qty=data.get('qty'),
            retail_price=data.get('retail_price'),
            wholesale_price=data.get('wholesale_price'),
            mfd_date=data.get('mfd_date'),
            exp_date=data.get('exp_date')
        )

        db_session.add(item)
        db_session.commit()

        item = Items.query.filter(
            Items.item_code == data.get('item_code')).first()

        return item_schema.jsonify(item)

    def delete(self, item_code):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        item = Items.query.filter(Items.item_code == item_code).first()

        if not item:
            abort(404)

        db_session.delete(item)
        db_session.commit()

        return response('success', 'Successfully deleted the item from Items with Id ' + str(item_code), 200)

    def put(self, item_code):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        item = Items.query.filter(Items.item_code == item_code).first()

        if not item:
            abort(404)

        data = request.get_json()

        item.item_code = data.get('item_code')
        item.name = data.get('name')
        item.qty = data.get('qty')
        item.retail_price = data.get('retail_price')
        item.wholesale_price = data.get('wholesale_price')
        item.mfd_date = data.get('mfd_date')
        item.exp_date = data.get('exp_date')

        db_session.commit()

        return response('success', 'Successfully updated the item from Items with Id ' + str(item_code), 200)
