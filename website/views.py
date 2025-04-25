from flask import Blueprint, render_template, flash,redirect, url_for, jsonify, request
from flask_login import login_required, current_user 
from . import db
from .models import Note
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)      # attach the current user to the template

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes(): 
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added successfully!", category='message')

    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=['DELETE'])
@login_required
def delete_note():
    note = json.loads(request.data)     # expects a JSON oject
    noteId = note['noteId']     # get the noteID from the note object
    note = Note.query.get(noteId)
    if note:        # check if note exists
        if note.user_id == current_user.id:     # check if the note belongs to current user
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted successfully!", category='message')
        else:
            flash("You do not have permission to delete this note.", category='error')
    else:
        flash("Note does not exist.", category='error')
    return jsonify({})  # Return an empty JSON response

