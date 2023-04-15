from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models import user
from flask_app.models import climb
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def initial():
    return redirect('/login_register')

@app.route('/login_register')
def home():
    return render_template('index.html')

@app.route('/register_user', methods=['POST'])
def new_user():
    if not user.User.validate(request.form):
        return redirect('/')
    data = {
        "user_name": request.form['user_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = user.User.save(data)
    session['user_id'] = id
    return redirect('/user_dashboard')

@app.route('/login',methods=['POST'])
def login():
    current_user = user.User.get_with_email(request.form)
    if not current_user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(current_user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = current_user.id
    return redirect('/user_dashboard')

@app.route('/user_dashboard')
def show_dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html" ,user=user.User.get_one(data), climbs=climb.Climb.get_all(data)) 


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")