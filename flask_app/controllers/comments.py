from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models import user
from flask_app.models import climb, comment

@app.route('/add_comment', methods=['POST'])
def add_comment():
    id = request.form['climb_id']
    if not comment.Comment.validate(request.form['comment']):
        return redirect(f'/details/{id}')
    data = {
        'comment' : request.form['comment'],
        'user_id' : request.form['user_id'],
        "climb_id" : request.form['climb_id']
    }
    comment.Comment.save(data)
    return redirect(f'/details/{id}')

@app.route('/delete/comment/<int:climb_id>/<int:id>')
def delete_comment(climb_id, id):
    data = {
        'id' : id
    }
    comment.Comment.delete(data)
    return redirect(f'/details/{climb_id}')
