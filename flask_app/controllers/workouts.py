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
    details = request.form.get('detail')

    if not workout_type:
        flash('Workout type is required', 'workout')
        return redirect('/workout/new')
    
    if not details:
        flash('Details are required', 'workout')
        return redirect('/workout/new')

    if len(details) < 20:
        flash('Details must be at least 20 characters long', 'workout')
        return redirect('/workout/new')

    workout_data = {
        'workout_type': workout_type,
        'details': details,
        'user_id': session['user_id']
    }
    Workout.create(workout_data)

    flash('Your workout has been added.', 'workout')
    return redirect('/report/dashboard')