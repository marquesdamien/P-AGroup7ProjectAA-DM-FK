from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.workout import Workout

@app.route('/workout/new')
def create_workout():
    if 'user_id' not in session:
        flash('Please login first', 'workout')
        return redirect('/')
    return render_template('create.html')

@app.route('/workout/new', methods=['POST'])
def add_workout():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect('/')

    workout_type = request.form.get('workout')
    workout_details = request.form.get('workout_detail')
    workout_date = request.form.get('workout_date')
    workout_name = request.form.get('workout_name')

    if not workout_type:
        flash('Workout type is required', 'workout')
        return redirect('/workout/new')
    
    if not workout_date:
        flash('Workout date is required', 'workout')
        return redirect('/workout/new')
    
    if len(workout_name) < 5:
        flash('Details must be at least 5 characters long', 'workout')
        return redirect('/workout/new')
    
    if len(workout_details) < 20:
        flash('Details must be at least 20 characters long', 'workout')
        return redirect('/workout/new')

    workout_data = {
        'workout_date': workout_date,
        'workout_type': workout_type,
        'workout_details': workout_details,
        'workout_name': workout_name,
        'user_id': session['user_id'],
    }
    Workout.create(workout_data)

    flash('Your workout has been added.', 'workout')
    return redirect('/report/dashboard')