import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import face_recognition
import sqlite3
import pickle
import numpy
import base64



# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ''
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Connect the database
conn = sqlite3.connect('faces.db')
c = conn.cursor()

known_face_encodings = []
known_face_names = []

c.execute("SELECT name, encoding FROM users")
known_faces = c.fetchall()
for face in known_faces:
    known_face_encodings.append(pickle.loads(face[1])[0])
    known_face_names.append(face[0])

conn.close()

name = "Unknown"

@app.route("/")
def index():
    return redirect("/welcome")

@app.route("/welcome")
def welcome():
    global name
    user = name
    name = "Unknown"
    if user == name:
        return redirect("/login")
    else:
        user = user.replace(',','').split()
        return render_template("welcome.html", name=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        global name
        blob = request.data
        with open('image.jpg', 'wb') as fh:
            # Get only revelant data, deleting "data:image/png;base64,"
            data = blob.split(',')[1]
            fh.write(base64.decodestring(data))
        # image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
        file = face_recognition.load_image_file('image.jpg')
        encoding = face_recognition.face_encodings(file)

        os.remove('image.jpg')

        if encoding:
            distances = face_recognition.face_distance(known_face_encodings, encoding[0])

            # If a match was found in known_face_encodings, just use the first one.
            if min(distances) < 0.4:
                match_index = numpy.where(distances == min(distances))[0][0]
                name = known_face_names[match_index]
            print(min(distances))
            print(name)
            return "match"
        return "no match"

    return render_template("login.html")


# @app.route("/check", methods=["POST"])
# def check():
#     """Check if a face is in the crowd"""
#     global name
#     blob = request.data
#     with open('image.jpg', 'wb') as fh:
#         # Get only revelant data, deleting "data:image/png;base64,"
#         data = blob.split(',')[1]
#         fh.write(base64.decodestring(data))
#     # image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
#     file = face_recognition.load_image_file('image.jpg')
#     encoding = face_recognition.face_encodings(file)
#
#     os.remove('image.jpg')
#
#     if encoding:
#         distances = face_recognition.face_distance(known_face_encodings, encoding[0])
#
#         # If a match was found in known_face_encodings, just use the first one.
#         if min(distances) < 0.5:
#             match_index = numpy.where(distances == min(distances))[0][0]
#             print(match_index)
#             name = known_face_names[match_index]
#         print(min(distances))
#         print(name)
#     return jsonify(True)


@app.route("/register", methods=["GET", "POST"])
def selfie():
    """Upload a picture"""
    if request.method == "POST":
        blob = request.form['userpic']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = lastname + ", " + firstname

        with open('add.jpg', 'wb') as fh:
            # Get only revelant data, deleting "data:image/png;base64,"
            data = blob.split(',')[1]
            fh.write(base64.decodestring(data))

        file = face_recognition.load_image_file('add.jpg')
        encoding = face_recognition.face_encodings(file)

        os.remove('add.jpg')

        if encoding and firstname and lastname:
            conn = sqlite3.connect('faces.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (name, encoding) VALUES (?, ?)",
                      (username, pickle.dumps(encoding)))
            conn.commit()
            conn.close()

            known_face_encodings.append(encoding[0])
            known_face_names.append(username)

            return "/login"
        else:
            return "error"

    return render_template("register.html")


# @app.route("/add", methods=["POST"])
# def add():
#     """Check if a face is in the crowd"""
#     blob = request.form['userpic']
#     firstname = request.form['firstname']
#     lastname = request.form['lastname']
#     username = lastname + ", " + firstname
#
#     with open('add.jpg', 'wb') as fh:
#         # Get only revelant data, deleting "data:image/png;base64,"
#         data = blob.split(',')[1]
#         fh.write(base64.decodestring(data))
#
#     file = face_recognition.load_image_file('add.jpg')
#     encoding = face_recognition.face_encodings(file)
#
#     os.remove('add.jpg')
#
#     if encoding:
#         conn = sqlite3.connect('faces.db')
#         c = conn.cursor()
#         c.execute("INSERT INTO users (name, encoding) VALUES (?, ?)",
#                   (username, pickle.dumps(encoding[0])))
#         conn.commit()
#         conn.close()
#
#         known_face_encodings.append(encoding[0])
#         known_face_names.append(username)
#
#     return jsonify(True)

#
# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)
