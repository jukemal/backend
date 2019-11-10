from api import ma
from api.items.models import Items,Stock


class ItemsSchema(ma.ModelSchema):
    class Meta:
        model = Items


item_schema = ItemsSchema(many=False)
items_schema = ItemsSchema(many=True)


class StockSchema(ma.ModelSchema):
    class Meta:
        model = Stock

    item_name = ma.Function(lambda obj: obj.item.name)


stock_schema = StockSchema(many=False)
stocks_schema = StockSchema(many=True)
