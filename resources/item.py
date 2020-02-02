from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="this field cannot be left blank")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"Item not found"}

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message":"Item already exists"},400

        data = Item.parser.parse_args()
        item = ItemModel(name,data['price'],data['store_id'])
        item.save_to_db()
        return item.json(),201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message":"Item has been deleted"}
        return {"message":"Item does not exists"},400

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name,data['price'],data['store_id'])
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {"items":[item.json() for item in ItemModel.query.all()]}

