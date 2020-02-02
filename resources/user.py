from flask_restful import Resource,reqparse
from flask import request
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="this field cannot be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":"Please choose a different username"}

        user = UserModel(data['username'],data['password'])
        user.save_to_db()
        return {"messaage":"User is registered successfully"},201


