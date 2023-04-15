from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, climb

class Comment:
    def __init__(self,data):
        self.id = data['id']
        self.comment = data['comment']
        self.climb_id = data['climb_id']
        self.user_id = data['user_id']

    @staticmethod
    def validate(comment):
        is_valid = True
        if len(comment) < 4:
            flash('comments must be 4 characters or more', 'comment')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO comments (comment, climb_id, user_id) VALUES (%(comment)s, %(climb_id)s, %(user_id)s);"
        return connectToMySQL('solo').query_db(query,data)
    
    @classmethod
    def get_comments_for_climb(cls,data):
        query = "SELECT * FROM comments JOIN users on comments.user_id = users.id where climb_id = %(id)s"
        results = connectToMySQL('solo').query_db(query,data)
        all_comments= []
        for row in results:
            one_comment = cls(row)
            posted_by_info = {
                'id' : row['users.id'],
                'user_name' : row['user_name'],
                'email' : row['email'],
                'password' : row['password']
            }
            posted_by = user.User(posted_by_info)
            one_comment.posted_by = posted_by
            all_comments.append(one_comment)
        return all_comments

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM comments where id = %(id)s;"
        return connectToMySQL('solo').query_db(query,data)
    









    