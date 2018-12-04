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

# files = os.listdir('people')
# if '.DS_Store' in files:
#     files.remove('.DS_Store')
#
# # Create arrays of known face encodings and their names
# known_face_encodings = []
# known_face_names = []
#
# for file in files:
#     image = face_recognition.load_image_file('people/' + file)
#     known_face_encodings.append(face_recognition.face_encodings(image)[0])
#     known_face_names.append(file.replace('.jpg',''))

# print(known_face_names)
# print(known_face_encodings)

name = "Unknown"

@app.route("/")
def index():
    return redirect("/login")

# @app.route("/upload", methods=["GET", "POST"])
# def upload():
#     """Upload a picture"""
#     global name
#     if request.method == "POST":
#         image = request.files["image"]
#         image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
#         file = face_recognition.load_image_file('image.jpg')
#         encoding = face_recognition.face_encodings(file)[0]
#
#         # matches = face_recognition.compare_faces(known_face_encodings, encoding, 0.5)
#         #
#         # print(matches)
#         # # If a match was found in known_face_encodings, just use the first one.
#         # if True in matches:
#         #     first_match_index = matches.index(True)
#         #     name = known_face_names[first_match_index]
#         #     return redirect("/welcome")
#
#         distances = face_recognition.face_distance(known_face_encodings, encoding)
#
#         # print(min(distances))
#         # If a match was found in known_face_encodings, just use the first one.
#         if min(distances) < 0.45:
#             match_index = numpy.where(distances == min(distances))[0][0]
#             name = known_face_names[match_index]
#             return redirect("/welcome")
#
#
#         os.remove('image.jpg')
#         return render_template("finalproject.html")
#
#     return render_template("finalproject.html")

<<<<<<< HEAD
@app.route("/harvard", methods=["GET"])
def welcome():
    global name
    user = name
    name = "Unknown"
    if user == name:
        return render_template("finalproject.html")
=======
@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        global name
        user = name
        name = "Unknown"
        if user == name:
            return redirect("/login")
        else:
            user = user.replace(',','').split()
        return render_template("welcome.html", name=user)
>>>>>>> 52cdf668d62f737b825f30e40ae431efbc825c42
    else:
        return redirect("/login")

# @app.route("/login")
# def login():
#     return render_template("finalproject.html")

@app.route("/check", methods=["POST"])
def check():
    global name
    """Check if a face is in the crowd"""
    blob = request.data
    with open('image.jpg', 'wb') as fh:
        # Get only revelant data, deleting "data:image/png;base64,"
        data = blob.split(',')[1]
        fh.write(base64.decodestring(data))
    # image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
    file = face_recognition.load_image_file('image.jpg')
    if face_recognition.face_encodings(file)[0]:
        encoding = face_recognition.face_encodings(file)[0]

    os.remove('image.jpg')

    distances = face_recognition.face_distance(known_face_encodings, encoding)
    print(min(distances))
    print(known_face_names[numpy.where(distances == min(distances))[0][0]])

    # If a match was found in known_face_encodings, just use the first one.
    if min(distances) < 0.5:
        match_index = numpy.where(distances == min(distances))[0][0]
        name = known_face_names[match_index]
    #     return jsonify(True)
    #
    # # match_index = numpy.where(distances == min(distances))[0][0]
    # # name = known_face_names[match_index]
    # else:
    #     return jsonify(False)


@app.route("/emot")
def selfie():
    """Upload a picture"""
    return render_template("emot.html")

#
# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)
# conn.close()
