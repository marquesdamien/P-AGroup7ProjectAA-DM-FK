from flask_app.config.mysqlconnection import connect

class Workout:
    DB = 'workout_tracker'
    
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO workouts (workout_type, details, user_id)
        VALUES (%(workout_type)s, %(details)s, %(user_id)s);
        """
        result = connect(cls.DB).query_db(query, data)
        return result