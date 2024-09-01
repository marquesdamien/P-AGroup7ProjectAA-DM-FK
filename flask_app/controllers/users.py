from flask_app import app
from flask import render_template, request, redirect, session, flash # type: ignore
from flask_app.models.user import User
from flask_bcrypt import Bcrypt   # type: ignore
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/register', methods=['POST'])
def users_register():
    print(f"request.form: {request.form}")
    if User.validator(request.form):   
        user_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        user_id = User.create(user_data)
        session['user_id'] = user_id     
        return redirect('/')
      
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def login():
    user_in_db = User.get_by_email({"email" : request.form["email"] })
    if user_in_db:
        if bcrypt.check_password_hash(user_in_db.password, request.form['password']):       
            session['user_id'] = user_in_db.id
            session['user_name'] = f"{user_in_db.first_name} {user_in_db.last_name}"
            return redirect('/report/dashboard')       
    flash("Invalid Credentials", 'login')
    return redirect("/")

@app.route('/users/logout')
def clear_session():
    session.clear   
    return redirect('/')