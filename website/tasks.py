from flask import Blueprint, render_template, flash,redirect, url_for, jsonify, request
from flask_login import login_required, current_user 
from . import db
from .models import Task
import json

tasks = Blueprint('tasks', __name__)

@tasks.route('/')       # Rendering route for task page
@login_required
def task_page():        # cannot be same name as blueprint name
    return render_template("tasks.html", user=current_user)

@tasks.route('/add', methods=['POST'])       # Route to add a new task, need to write "methods"
@login_required
def add_task():
    title = request.form.get('title')    
    description = request.form.get('description')

    if title is None or description is None:     # check if title and description are not empty
        flash("Task title or description cannot be empty!", category='error')
    elif len(title) < 1 or len(description) < 1:
        flash("Task title or description is too short!", category='error')
    else:
        new_task = Task(title=title, description=description, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", category='message')   

    return redirect(url_for('tasks.task_page'))

@tasks.route('/update', methods=['PUT'])       # Route to update a task
@login_required
def update_task():
    data = request.get_json()
    task_id = data.get('taskId')
    new_title = data.get('title')
    new_description = data.get('description')

    task = Task.query.get(task_id)
    if task:        # check if task exists
        if task.user_id == current_user.id:     # check if the task belongs to current user
            task.title = new_title
            task.description = new_description
            db.session.commit()
            flash("Task updated successfully!", category='message')
        else:
            flash("You do not have permission to update this task.", category='error')
    else:
        flash("Task does not exist.", category='error')
    return jsonify({})  # Return an empty JSON response


@tasks.route('/delete', methods=['DELETE'])       # Route to delete a task
@login_required
def done_task():
    task = json.loads(request.data)     # expects a JSON object
    taskId = task['taskId']             # get the taskID from the task object
    task = Task.query.get(taskId)
    if task:        # check if task exists
        if task.user_id == current_user.id:     # check if the task belongs to current user
            db.session.delete(task)
            db.session.commit()
            flash("Task deleted successfully!", category='message')
        else:
            flash("You do not have permission to delete this task.", category='error')
    else:
        flash("Task does not exist.", category='error')
    return jsonify({})  # Return an empty JSON response