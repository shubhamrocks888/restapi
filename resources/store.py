from flask_restful import Resource,reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="this field cannot be left blank")

    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message":"store not found"},404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {"message":"Store already exists"},400

        data = Store.parser.parse_args()
        store = StoreModel(name)
        store.save_to_db()
        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message":"Store has been deleted"}
        return {"message":"Store does not exists"},400

class StoreList(Resource):
    def get(self):
        return {"Stores":[store.json() for store in StoreModel.find_all()]}

