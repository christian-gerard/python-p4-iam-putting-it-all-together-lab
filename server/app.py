#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe
import ipdb


class Signup(Resource):

    def post(self):
        try: 
            data = request.get_json()
            if data.get('username'):
                new_user = User(username=data.get('username'), image_url=data.get('image_url'), bio=data.get('bio'))
            else:
                return {"error":"CANT DO THAT"}, 422

            if dup_name := User.query.filter_by(username=data.get('username')).first():
                return {"error": "Invalid input"}, 422


            if isinstance(new_user, User):
                new_user.password_hash = data.get('password')
                db.session.add(new_user)
                db.session.commit()

                session['user_id'] = new_user.id
                return data, 200
            
        except Exception as e:
            return str(e), 400
        

class CheckSession(Resource):
    def get(self):
        try:
            current_user = session.get('user_id')

            user = User.query.filter_by(id = current_user).first()

            return user.to_dict(), 200
        
        except Exception as e:
            return {"error": "User is not logged in"}, 401

class Login(Resource):
    def post(self):
        try:
            data = request.json
            user = User.query.filter_by(username=data.get('username')).first()
            if user and user.authenticate(data.get('password')):
                session['user_id'] = user.id
                return user.to_dict(), 200
            else:
                return {"message": "Invalid Credentials"}, 401
            
        except Exception as e:
            return {"message": str(e)}, 422

class Logout(Resource):
    def delete(self):
        try:
            if session.get('user_id'):
    
                session['user_id'] = None
                return {}, 204
            else:
                return {"error": "No user is logged in"}, 401
        
        except Exception as e:

            return {"error": str(e)}, 400

class RecipeIndex(Resource):
    def get(self):
        try:
            if id := session.get('user_id'):
                recipes = [recipe.to_dict() for recipe in Recipe.query.filter(Recipe.user_id == id).all()]
                return recipes, 200
            else:
                return {'Error' : 'User not logged in'}, 401

        except Exception as e:
            return {'error' : str(e)}, 401
        
    def post(self):
        try:
            if id := session.get('user_id'):
                data = request.get_json()
                new_recipe = Recipe(instructions=data.get('instructions'), minutes_to_complete=data.get('minutes_to_complete'), title=data.get('title'), user_id=id)

                db.session.add(new_recipe)
                db.session.commit()

                return new_recipe.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 422


api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)