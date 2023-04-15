from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models import user
from flask_app.models import climb, comment
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/add_climb', methods=['POST'])
def add_climb():
    if not climb.Climb.validate(request.form):
        return redirect('/user_dashboard')
    data = {
        'name' : request.form['name'],
        'location' : request.form['location'],
        'description' : request.form['description'],
        'rating' : request.form['rating'],
        'posted_by' : request.form['posted_by']
    }
    climb.Climb.save(data)
    return redirect('/user_dashboard')

@app.route('/details/<int:id>')
def view_one_climb(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template('climb_details.html', climb=climb.Climb.get_one(data), user=user.User.get_one(user_data), comments=comment.Comment.get_comments_for_climb(data), check_climb=climb.Climb.check_if_climbed(data))

@app.route('/user_climbs/<int:id>')
def view_my_climbs(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    return render_template('user_climbs.html', climbs=climb.Climb.get_climbs_from_user(data), user=user.User.get_one(data))

@app.route('/add_to_user_climbs', methods=['POST'])
def add_to_user_climbs():
    climb_id = request.form['climb_id']
    data = {
        'user_id' : request.form['user_id'],
        'climb_id' : climb_id
    }
    user.User.add_user_to_climb(data)
    return redirect(f'/details/{climb_id}')

@app.route('/climb_edit_form/<int:id>')
def edit_climb_form(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    if session['user_id'] != climb.Climb.get_one(data).posted_by:
        return redirect('/user_dashboard')
    user_data = {
        'id' : session['user_id']
    }
    return render_template('edit_form.html', climb= climb.Climb.get_one(data), user=user.User.get_one(user_data))

@app.route('/update_climb/<int:id>', methods=["POST"])
def update(id):
        if not climb.Climb.validate(request.form):
            return redirect(f'/climb_edit_form/{id}')
        data = {
            'id' : id,
            'name' : request.form['name'],
            'location' : request.form['location'],
            'description' : request.form['description'],
            'rating' : request.form['rating'],
            'posted_by' : request.form['posted_by']
        }
        climb.Climb.update(data)
        return(redirect(f'/details/{id}'))

@app.route('/delete/climb/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    if session['user_id'] != climb.Climb.get_one(data).posted_by:
        return redirect('/user_dashboard')
    climb.Climb.delete(data)
    return (redirect('/user_dashboard'))