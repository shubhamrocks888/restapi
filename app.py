from flask import Flask,request
from flask_restful import Resource,Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self,name):
        item = next(filter(lambda x:x['name']==name,items),None)
        return {'item':item},200 if item else 404

    def post(self,name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            return {"message":"item already exists"},400
        data = request.get_json()
        new_item = {'name':name,'price':data['price']}
        items.append(new_item)
        return new_item,201

class ItemList(Resource):
    def get(self):
        return {"items":items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items/')


app.run(port=5000,debug=True)