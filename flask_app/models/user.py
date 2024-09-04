from flask_app import app
from flask_app.config.mysqlconnection import connect
from flask import flash, session   

import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')        
PASSWOED_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$") 


class User:
    DB = 'workout_tracker'
    def __init__(self, data):
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_id(cls, user_id):
        query = """
        SELECT * FROM users
        WHERE user_id = %(user_id)s
        """
        data = {'user_id': user_id}
        results = connect(cls.DB).query_db(query, data)
        print(results)
        return cls(results[0]) if results else None
        
    @staticmethod
    def validator(form_data):
        is_valid = True
       
        if not form_data['first_name'].strip():
            is_valid = False
            flash('First Name Required', 'registration')
      
        elif len(form_data['first_name']) < 2:
            is_valid = False
            flash('2 Char Min', 'registration')

        if not form_data['last_name'].strip():
            is_valid = False
            flash('First Name Required', 'registration')
       
        elif len(form_data['last_name']) < 2:
            is_valid = False
            flash('2 Char Min', 'registration')

        if not form_data['email'].strip():
            is_valid = False
            flash('Email Required', 'registration')
        
        elif not EMAIL_REGEX.match(form_data['email']):
            is_valid = False
            flash('Invalid Email', 'registration')
       
        elif User.get_by_email(form_data):
            is_valid = False
            flash('Email In Use', 'registration')
       
        if not form_data['password'].strip():
            is_valid = False
            flash('Password Required', 'registration')
       
        elif len(form_data['password']) < 8:
            is_valid = False
            flash('8 Char Min', 'registration')

        elif form_data['password'] != form_data['conf_password']:
            is_valid = False
            flash('Passwords Must Match', 'registration')
        
        return is_valid
    
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connect(cls.DB).query_db(query, data)
        print(results)
        if not results:
            return False
        
        return cls(results[0])
    
    @classmethod
    def create(cls, form_data):
        print(f"model: {form_data}")
        query = """
        INSERT INTO users 
        (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        user_id = connect(cls.DB).query_db(query, form_data)
        return user_id
    
    @classmethod
    def login(cls, data):
        this_user = cls.get_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.user_id
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                return True
        flash('Your login information was incorrect')
        return False