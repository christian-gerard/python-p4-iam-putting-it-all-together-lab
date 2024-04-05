
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import func
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', back_populates='user')

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        if not password:
            self._password_hash = self.simple_hash(password)
        else:
            raise AttributeError('Cant Change password')
  

    def authenticate(self, password):
        return self.simple_hash(password) == self.password_hash

    @staticmethod
    def simple_hash(input):
        return sum(bytearray(input, encoding='utf-8'))

class Recipe(db.Model, SerializerMixin):

    __tablename__ = 'recipes'
    __table_args__ = (db.CheckConstraint('length(instructions) >= 50'),)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='recipes')
    
    def __repr__(self):
        return f'<Recipe {self.id}: instructions"{self.instructions}">'


