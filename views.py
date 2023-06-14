from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from datetime import datetime, timedelta

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note') #Gets the note from the HTML

        if not note:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Task added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/rewards')
def rewards():
    return "This is the rewards page."

@views.route('/timer')
@login_required
def index():
    return render_template('index.html')

@views.route('/start_timer', methods=['POST'])
@login_required
def start_timer():
    minutes = int(request.form['duration'])
    duration = minutes * 60
    end_time = datetime.now() + timedelta(seconds=duration)
    return render_template('timer.html', end_time=end_time)

@views.route('/countdown/<end_time>')
def countdown(end_time):
    end_time = datetime.fromisoformat(end_time)
    remaining_time = end_time - datetime.now()
    if remaining_time.total_seconds() <= 0:
        remaining_time = timedelta(seconds=0)
    return render_template('countdown.html', remaining_time=remaining_time)

