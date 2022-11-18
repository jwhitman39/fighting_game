import this
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, game
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

class Fighter:
    db_name='games_users_and_fighters_schema'
    def __init__(self, data):
        self.id=data['id']
        self.name=data['name']
        # self.strength=data['strength']
        # self.speed=data['speed']
        # self.health=data['health']
        self.description=data['description']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user=None
        self.type =None

    @classmethod
    def add_fighter_to_db (cls, data):
        query="INSERT INTO fighters (name, type_id, description, user_id) VALUES (%(name)s, %(type_id)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_fighters_with_users(cls):
        query='SELECT * FROM fighters JOIN users ON fighters.user_id = users.id;'
        results=connectToMySQL(cls.db_name).query_db(query)
        print('Got data')
        if len(results) == 0:
            return []
        else:
            all_fighter_instances = [] #hold all fighters
            for this_fighter_dictionary in results:
                this_fighter_instance=cls(this_fighter_dictionary)
                this_user_dictionary={
                    'id' : this_fighter_dictionary['users.id'],
                    'first_name' : this_fighter_dictionary['first_name'],
                    'last_name' : this_fighter_dictionary['last_name'],
                    'email' : this_fighter_dictionary['email'],
                    'password' : this_fighter_dictionary['password'],
                    'created_at' : this_fighter_dictionary['users.created_at'],
                    'updated_at' : this_fighter_dictionary['users.updated_at']
                }
                this_user_instance=user.User(this_user_dictionary)
                this_fighter_instance.user = this_user_instance
                all_fighter_instances.append(this_fighter_instance)
            return all_fighter_instances

    @staticmethod
    def validate_fighter(form_data):
        is_valid=True
        print('validation started:')
        print(form_data)
        print('Price is fine')
        if len(form_data['name'])<3:
            is_valid=False
            flash('name needs to be at least three characters!')
            print('something is wrong with the name')
        print('name is fine')
        print('type is fine')
        if len(form_data['description'])<3:
            is_valid=False
            flash('Description must be at least three characters')
            print('Description must be at least three characters')
        print('Description is fine')
        print('successful validation!')
        return is_valid