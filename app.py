import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
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

# Make a list to hold the encodings and names of the students
known_face_encodings = []
known_face_names = []

# Get all names and encodings as a list
c.execute("SELECT name, encoding FROM users")
known_faces = c.fetchall()

# Iterate over the list, saving the encodings and faces
for face in known_faces:
    known_face_encodings.append(pickle.loads(face[1])[0])
    known_face_names.append(face[0])

# Close the database
conn.close()

# Set a global variable, name
name = "Unknown"

@app.route("/")
def index():
    return redirect("/welcome")

# Landing page for "logged-in" users
@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        global name
        # Save the value of name and reset it to unknown
        user = name
        name = "Unknown"

        # If name was originally its default value, go back to the login page.
        if user == name:
            return redirect("/login")
        # Else, if a user has been identified, welcome them.
        else:
            # name is stored in the database as "Lastname, Firstname"
            user = user.replace(',','').split()
            return render_template("welcome.html", name=user)
    # else if it's a post request, (click on sign out or homepage), redirect
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If a user submits a photo via POST
    if request.method == "POST":
        # Save a copy of the picture they sent in the current directory
        with open('image.jpg', 'wb') as fh:
            # Get only revelant data, deleting "data:image/png;base64,"
            data = request.data.split(',')[1]
            fh.write(base64.decodestring(data))
        # Load and encode the image
        file = face_recognition.load_image_file('image.jpg')
        encoding = face_recognition.face_encodings(file)

        # Delete our copy of the picture
        os.remove('image.jpg')

        # If a face was found, find the closest recognized face in the database.
        if encoding:
            distances = face_recognition.face_distance(known_face_encodings, encoding[0])

            # If there is a close match, set name to the name of the recognized user.
            if min(distances) < 0.4:
                match_index = numpy.where(distances == min(distances))[0][0]
                global name
                name = known_face_names[match_index]
                print(name)
                print(min(distances))
                return "match"
        return "no match"
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def selfie():
    """Upload a picture"""
    # If the user submits the form via post...
    if request.method == "POST":
        # Get their first and last names and make a username of the form "Lastname, Firstname"
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = lastname + ", " + firstname

        # Save a copy of the picture they sent
        with open('add.jpg', 'wb') as fh:
            # Get only revelant data, deleting "data:image/png;base64,"
            data = request.form['userpic'].split(',')[1]
            fh.write(base64.decodestring(data))

        # Encode the picture of their face
        file = face_recognition.load_image_file('add.jpg')
        encoding = face_recognition.face_encodings(file)

        # Get rid of our copy of the picture
        os.remove('add.jpg')

        # If they sent all the required data, add it to the database and list of names/encodings.
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
