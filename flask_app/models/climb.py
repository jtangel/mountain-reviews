from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import climb

class Climb:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.description = data['description']
        self.rating = data['rating']
        self.posted_by = data['posted_by']
        self.users = []

    @staticmethod
    def validate(climb):
        is_valid = True
        if len(climb['name']) < 4:
            flash("Route Name must be 4 or more characters", 'climb')
            is_valid = False
        if len(climb['location']) < 4:
            flash("Location must be 4 or more characters", 'climb')
            is_valid = False
        if len(climb['description']) <= 10:
            flash("Description must be longer than 10 characters", 'climb')
            is_valid = False
        if climb['rating'] != '1' and climb['rating'] != '2' and climb['rating'] != '3' and climb['rating'] != '4' and climb['rating'] != '5':
            flash("Rating must be in between 1 and 5", 'climb')
            is_valid = False
        if len(climb['rating']) < 1:
            flash("Rating is required", 'climb')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO climbs (name, location, description, rating, posted_by, created_at, updated_at) VALUES (%(name)s, %(location)s, %(description)s, %(rating)s, %(posted_by)s, NOW(), NOW());"
        return connectToMySQL('solo').query_db(query,data)
    
    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM climbs;"
        results = connectToMySQL('solo').query_db(query,data)
        all_climbs = []
        for row in results:
            one_climb = cls(row)
            all_climbs.append(one_climb)
        return all_climbs

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM climbs JOIN users on climbs.posted_by = users.id WHERE climbs.id = %(id)s;"
        result = connectToMySQL('solo').query_db(query,data)
        result = result[0]
        climb = cls(result)
        climb.climber = user.User (
            {
                'id' : result['users.id'],
                'user_name' : result['user_name'],
                'email' : result['email'],
                'password' : result['password']
            }
        )
        return climb

    @classmethod
    def get_climbs_from_user(cls,data):
        query= "SELECT * FROM users_who_climbed JOIN users on users_who_climbed.user_id = users.id JOIN climbs on users_who_climbed.climb_id = climbs.id where users.id = %(id)s;"
        results = connectToMySQL('solo').query_db(query,data)
        users_climbs = []
        for row in results:
            one_climb = cls(row)
            climb_info = {
                'id' : row['climbs.id'],
                'name' : row['name'],
                'location' : row['location'],
                'description' : row['description'],
                'rating' : row['rating'],
                'posted_by' : row['posted_by']
            }
            climb_specific = climb.Climb(climb_info)
            one_climb.climb_specific = climb_specific
            users_climbs.append(one_climb)
        print(users_climbs)
        return users_climbs

    @classmethod
    def update(cls,data):
        query = 'UPDATE climbs SET name = %(name)s, location = %(location)s, description = %(description)s, rating = %(rating)s, posted_by = %(posted_by)s, updated_at = NOW() where id=%(id)s;'
        return connectToMySQL('solo').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = 'DELETE from climbs where id = %(id)s;'
        return connectToMySQL('solo').query_db(query,data)
    
    @classmethod
    def check_if_climbed(cls,data):
        query = "SELECT * FROM users_who_climbed where climb_id = %(id)s;"
        print(connectToMySQL('solo').query_db(query,data))
        # [{'climb_id': 1, 'user_id': 1}, {'climb_id': 1, 'user_id': 2}]
        results = connectToMySQL('solo').query_db(query,data)
        ids = []
        for row in results:
            ids.append(row['user_id'])
        print(ids)
        return ids