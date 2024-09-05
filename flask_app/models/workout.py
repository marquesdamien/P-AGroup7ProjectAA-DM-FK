from flask_app.config.mysqlconnection import connect
from flask_app.models import user
from flask import flash






class Workout:
    DB = 'workout_tracker'
    def __init__(self, data):
        self.workout_id = data['workout_id']
        self.workout_date = data['workout_date']
        self.workout_type = data['workout_type']
        self.workout_details = data['workout_details']
        self.workout_name = data['workout_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id =  data['user_id']
        self.creator = None


    @classmethod
    def validate_workout_data(cls, data):
        is_valid = True # we assume this is true
        if len(data['workout_name']) < 5:
            flash("Workout Name must be at least 3 characters.")
            is_valid = False
        if len(data['workout_details']) < 10:
            flash("Workout Details must be at least 10 characters.")
            is_valid = False
        if not data['workout_date']:
            flash('workout date is required')
            is_valid = False
        if not data['workout_type']:
            flash('Workout Type required')
            is_valid = False
        return is_valid
    
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO workouts (workout_date, workout_type, workout_details, workout_name, created_at, updated_at, user_id)
        VALUES (%(workout_date)s, %(workout_type)s, %(workout_details)s, %(workout_name)s, NOW(), NOW(), %(user_id)s);
        """
        result = connect(cls.DB).query_db(query, data)
        return result
    

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM workouts
        JOIN users on workouts.user_id = users.user_id;"""
        results = connect(cls.DB).query_db(query)
        workouts = []
        for workout in results:
            workout_obj = Workout(workout)
            user_obj = user.User({
                "user_id" : workout["users.user_id"],
                "first_name" : workout["first_name"],
                "last_name" : workout["last_name"],
                "email" : workout["email"],
                "created_at" : workout["users.created_at"],
                "updated_at" : workout["users.updated_at"],
                "password" : workout["password"] 
            })
            workout_obj.creator = user_obj
            workouts.append(workout_obj)
            print(results)
            print(workouts)
        return workouts
    
    @classmethod
    def get_one_by_workout_id(cls, workout_id):
        data = {
            "workout_id" : workout_id
        }
        query = """
            SELECT * FROM workouts
            JOIN users ON workouts.user_id = users.user_id
            WHERE workouts.workout_id = %(workout_id)s
            ;"""
        
        result = connect(cls.DB).query_db(query, data)
        this_workout = result[0]
        workout_obj = Workout(this_workout)
        user_obj = user.User({
            "user_id" : this_workout["users.user_id"],
            "first_name" : this_workout["first_name"],
            "last_name" : this_workout["last_name"],
            "email" : this_workout["email"],
            "created_at" : this_workout["users.created_at"],
            "updated_at" : this_workout["users.updated_at"],
            "password" : this_workout["password"] 
        })

        workout_obj.creator = user_obj

        return workout_obj
    

    @classmethod
    def update(cls, data):
        if not cls.validate_workout_data(data):
            return False
        query = """
        UPDATE workouts
        SET
            workout_date = %(workout_date)s,
            workout_type = %(workout_type)s,
            workout_details = %(workout_details)s,
            workout_name = %(workout_name)s
        WHERE workout_id = %(workout_id)s
        ;"""
        connect(cls.DB).query_db(query, data)
        print(query)
        return True
    

    @classmethod
    def delete_workout(cls, workout_id):
        data = {
            "workout_id" : workout_id
        }
        query = """
            DELETE FROM workouts
            WHERE workout_id = %(workout_id)s
        ;"""
        connect(cls.DB).query_db(query, data)
        return