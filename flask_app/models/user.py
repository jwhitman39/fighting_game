from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.controllers import fighters, games
from flask_app.models import fighter, game, user
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

class User:
    db_name='games_users_and_fighters_schema'
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.fighters=[]

    @classmethod
    def add_user_to_db (cls, data):
        query="INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one_user(cls, data):
        query="SELECT * FROM users WHERE id = %(id)s;"
        results=connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            print('no user found')
            return None
        else:
            print('user found')
            return cls(results[0])

    @classmethod
    def get_one_user_by_email(cls, data):
        query="SELECT * FROM users WHERE email = %(email)s;"
        results=connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results)==0:
            return None
        else:
            return cls(results[0])


    @staticmethod
    def validate_register(form_data):
        is_valid=True
        print('validation started')
        if len(form_data['first_name'])<3:
            is_valid=False
            flash('First name needs to be at least three characters!')
            print('something is wrong with the first name')
        if len(form_data['last_name'])<3:
            is_valid=False
            flash('Last name needs to be at least three characters!')
            print('something is wrong with the last name')
        if not EMAIL_REGEX.match(form_data['email']): 
            is_valid = False
            flash("This email address will not do!")
            print('something is wrong with the email')
        if len(form_data['password'])<8:
            is_valid=False
            flash('Password needs to be at least eight characters!')
            print('something is wrong with the password')
        if form_data['password']!=form_data['confirm_password']:
            is_valid=False
            flash('The passwords do not match!')
            print('the passwords are not matching')
        print('successful validation!')
        return is_valid

    @staticmethod
    def validate_login(form_data):
        is_valid=True
        print('login validation started')
        email_data={
            'email': form_data['email']
        }
        found_user_or_none= User.get_one_user_by_email(email_data)
        if not found_user_or_none:
            flash('Invalid login credentials')
            print('something is wrong with the email')
            return False
        if not bcrypt.check_password_hash(found_user_or_none.password, form_data['password']):
            flash('Invalid login credentials')
            print('something is wrong with the password')
            is_valid=False
        return is_valid