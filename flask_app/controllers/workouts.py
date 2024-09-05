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
    workout_details = request.form.get('workout_details')
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
    
    if len(workout_details) < 10:
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


@app.get('/workout/edit/<workout_id>')
def edit_page(workout_id):
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    print("in Edit page:" , workout_id)
    workout_viewed = Workout.get_one_by_workout_id(workout_id)
    if session['user_id'] != workout_viewed.user_id:
        flash("You do not have access to Another Users Workouts")
        return redirect('/')
    return render_template('edit_workout.html', workout = workout_viewed)

@app.route('/workout/update', methods=['POST'])
def edit_workout():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect('/')
    is_valid = Workout.validate_workout_data(request.form)
    if Workout.update(request.form):
        return redirect('/report/dashboard')
    print(request.form)
    print(is_valid)
    return redirect(f'/shows/edit/{request.form["workout_id"]}')

@app.route('/workout/delete/<workout_id>')
def delete_workout(workout_id):
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect('/')
    workout = Workout.get_one_by_workout_id(workout_id)
    if workout and workout.user_id == session['user_id']:
        Workout.delete_workout(workout_id)
        flash('Workout deleted.', 'success')
    return redirect('/report/dashboard')

@app.route('/workout/view/<int:workout_id>')
def view_workout(workout_id):
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect('/')
    workout = Workout.get_one_by_workout_id(workout_id)
    if workout and workout.user_id == session['user_id']:
        return render_template('view.html', workout=workout)
    return redirect('/report/dashboard')

