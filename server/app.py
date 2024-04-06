#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe
import ipdb

class Signup(Resource):

    def get(self):
        users = User.query.all()
        try:
            user_data = [ user.to_dict() for user in users]
            return user_data, 200
        except Exception as e:
            return str(e), 404

    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if User.query.filter(User.username == username).first():
            return {'message': 'Username already exists'}, 400
        
        hashed = User.password_hash(password)

        new_user = User(username=username, _password_hash=hashed)

        db.session.add(new_user)
        db.session.commit()

        return new_user, 200


            
        





class CheckSession(Resource):
    pass

class Login(Resource):
    pass

class Logout(Resource):
    pass

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)