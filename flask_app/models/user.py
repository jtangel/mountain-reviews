from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__(self,data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.email = data['email']
        self.password = data['password']
        self.climbs = []

    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('solo').query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email","register")
            is_valid=False
        if len(user['user_name']) < 3:
            flash("User name needs to be 3 characters or more","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password needs to be 8 characters or more","register")
            is_valid= False
        if user['password'] != user['confirm_pw']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (user_name, email, password, created_at, updated_at) VALUES (%(user_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('solo').query_db(query,data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('solo').query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_with_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('solo').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def add_user_to_climb(cls,data):
        query = "INSERT INTO users_who_climbed (user_id, climb_id) VALUES (%(user_id)s, %(climb_id)s);"
        return connectToMySQL('solo').query_db(query,data)