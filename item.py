from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="this field cannot be left blank")

    @jwt_required()
    def get(self,name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message":"Item not found"}

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert(cls,item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query,(item['name'],item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'], item['name']))
        connection.commit()
        connection.close()

    def post(self,name):
        if self.find_by_name(name):
            return {"message":"Item already exists"},400

        data = Item.parser.parse_args()
        item = {"name":name,"price":data['price']}
        try:
            self.insert(item)
        except:
            return {"message":"An error has occured during insertion of item"},500
        return item,201

    def delete(self,name):
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {"message":"Item has been deleted"}
        return {"message":"Item does not exists"},400

    def put(self,name):
        data = Item.parser.parse_args()
        updated_item = {"name": name, "price": data['price']}
        item = self.find_by_name(name)
        if item:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error has occured during updating of item"}, 500
        else:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error has occured during insertion of item"}, 500
        return updated_item

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name":row[0],"price":row[1]})
        connection.close()
        return {"items":items}

