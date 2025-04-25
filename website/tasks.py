from flask import Blueprint, render_template, flash,redirect, url_for, jsonify, request
from flask_login import login_required, current_user 
from . import db
from .models import Task
import json

tasks = Blueprint('tasks', __name__)

@tasks.route('/')       # Rendering route for task page
@login_required
def task_page():
    return render_template("tasks.html", user=current_user)

@tasks.route('/add', method='POST')
@login_required
def add_task():
    new_task = request.form.get('task')
    if len(new_task) < 1:
        flash("Task is too short!", category='error')
    else:
        new_task = Task(data=new_task, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", category='message')
    return redirect(url_for('tasks.home'))
