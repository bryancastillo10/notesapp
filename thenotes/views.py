from flask import Blueprint,render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from datetime import datetime 
from . import db
import json

views = Blueprint('views',__name__)

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!',category="success")
    
    example_datetime = datetime.now()
    formatted_datetime = format_datetime(example_datetime)

    notes = Note.query.order_by(Note.date.desc()).all()
    return render_template("home.html", user=current_user, formatted_datetime=formatted_datetime)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId= note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return Jsonify({})