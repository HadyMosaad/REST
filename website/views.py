from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Folder
from . import db
from flask import Blueprint, render_template, request, flash, redirect, url_for
import json

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    Folders = Folder.query.all()
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id, folder_id=0)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")

    return render_template("home.html", user=current_user, folders=Folders)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route("/add-folder", methods=["POST","GET"])
def add_folder():
    if request.method == "POST":
        name = request.form.get("name")
        typr = request.form.get("type")
        new_folder = Folder(name=name, typr=typr)
        db.session.add(new_folder)
        db.session.commit()
        flash("Folder created!", category="success")
        return redirect(url_for("views.home"))

    return render_template("addFolder.html", user=current_user)
