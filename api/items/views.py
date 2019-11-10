from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import abort
from sqlalchemy import func

from api.database import db_session

from api.items.models import Items,Stock
from api.items.Schema import item_schema, items_schema,stock_schema,stocks_schema

from api.helpers import response


class ItemsAPI(MethodView):
    def get(self, item_code):
        if item_code is None:
            items = Items.query.all()

            return items_schema.jsonify(items)
        else:
            item = Items.query.filter(Items.id_ == item_code).first()

            if not item:
                return response('Not Found', f'Item with Item Code {item_code} is not available.', 404)

            return item_schema.jsonify(item)

    def post(self):
        if not request.content_type == 'application/json':
            return response('Failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        fields = ['name']
        string = ''

        for i in fields:
            if not data.get(f'{i}'):
                string = string+f'\"{i}\", '

        if string:
            return response('Invalid POST Request', f'These fields should be included in the POST Request. {string}', 404)

        item = Items(
            name=data.get('name')
        )

        db_session.add(item)
        db_session.commit()

        return response('Added Successfully.', f'Successfully added the item with Item Code {str(item.id_)}', 200, item_schema.dump(item))

    def delete(self, item_code):

        item = Items.query.filter(Items.id_ == item_code).first()

        if not item:
            return response('Not Found', f'Item with Item Code {item_code} is not available.', 404)

        db_session.delete(item)
        db_session.commit()

        return response('Delete Successful.', f'Successfully deleted the Items with Item Code {str(item_code)}', 200, item_schema.dump(item))

    def put(self, item_code):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        item = Items.query.filter(Items.id_ == item_code).first()

        if not item:
            return response('Not Found', f'Item with Item Code {item_code} is not available.', 404)

        data = request.get_json()

        item.name = data.get('name')

        db_session.commit()

        return response('Update Successful.', f'Successfully updated the Items with Item Code {str(item_code)}', 200,item_schema.dump(item))


class StockAPI(MethodView):
    def get(self, id):
        if id is None:
            stock = Stock.query.all()

            report = Stock.query.with_entities(func.date_trunc("day", Stock.exp_date).label("date"), func.count(
                Stock.id_).label("count")).group_by(func.date_trunc("day", Stock.exp_date)).all()

            return jsonify(data=stocks_schema.dump(stock), report=report)
        else:
            stock = Stock.query.filter(Stock.id_ == id).first()

            if not stock:
                return response('Not Found', f'Item with Item Code {id} is not available.', 404)

            return stock_schema.jsonify(stock)

    def post(self):
        if not request.content_type == 'application/json':
            return response('Failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        fields = ['item_code', 'qty', 'retail_price',
                  'wholesale_price', 'mfd_date', 'exp_date']
        string = ''

        for i in fields:
            if not data.get(f'{i}'):
                string = string+f'\"{i}\", '

        if string:
            return response('Invalid POST Request', f'These fields should be included in the POST Request. {string}', 404)

        item = Items.query.filter(Items.id_ == data.get('item_code')).first()

        stock = Stock(
            item=item,
            qty=data.get('qty'),
            retail_price=data.get('retail_price'),
            wholesale_price=data.get('wholesale_price'),
            mfd_date=data.get('mfd_date'),
            exp_date=data.get('exp_date')
        )

        db_session.add(stock)
        db_session.commit()

        return response('Added Successfully.', f'Successfully added the item with Item Code {str(stock.id_)}', 200, stock_schema.dump(stock))

    def delete(self, id):

        stock = Stock.query.filter(Stock.id_ == id).first()

        if not stock:
            return response('Not Found', f'Item with Item Code {id} is not available.', 404)

        db_session.delete(stock)
        db_session.commit()

        return response('Delete Successful.', f'Successfully deleted the Items with Item Code {str(id)}', 200, stock_schema.dump(stock))

    def put(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        stock = Stock.query.filter(Stock.id_ == id).first()

        if not stock:
            return response('Not Found', f'Item with Item Code {id} is not available.', 404)

        data = request.get_json()

        if data.get('item_code'):
            item = Items.query.filter(Items.id_ == data.get('item_code')).first()
            stock.item=item

        if data.get("qty"):
            stock.qty = data.get('qty')

        if data.get("retail_price"):
                    stock.retail_price = data.get('retail_price')

        if data.get("wholesale_price"):
                    stock.wholesale_price = data.get('wholesale_price')

        if data.get("mfd_date"):
                    stock.mfd_date = data.get('mfd_date')

        if data.get("exp_date"):
                    stock.exp_date = data.get('exp_date')

        db_session.commit()

        return response('Update Successful.', f'Successfully updated the Items with Item Code {str(id)}', 200, stock_schema.dump(stock))
