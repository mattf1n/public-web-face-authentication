from os import remove
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from face_recognition import load_image_file, face_encodings, face_distance
from sqlite3 import connect
from pickle import loads, dumps
from numpy import where
from base64 import decodestring
from tempfile import mkdtemp


# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ''
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Connect the database
conn = connect('faces.db')
c = conn.cursor()

# Make a list to hold the encodings and names of the students
known_face_encodings = []
known_face_names = []

# Get all names and encodings as a list
c.execute("SELECT name, encoding FROM users")
known_faces = c.fetchall()

# Iterate over the list, saving the encodings and faces
for face in known_faces:
    known_face_encodings.append(loads(face[1])[0])
    known_face_names.append(face[0])

# Close the database
conn.close()

@app.route("/")
def index():
    return redirect("/welcome")

# Landing page for "logged-in" users
@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        # If name was originally its default value, go back to the login page
        if not session:
            return redirect("/login")

        # Else, if a user has been identified, welcome them.
        else:
            # name is stored in the database as "Lastname, Firstname"
            print(session['name'])
            name = session['name'].split(",")
            return render_template("welcome.html", name=name)

        # Close the database
        conn.close()

    # else if it's a post request, (click on sign out or homepage), redirect
    else:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    # clear user Session
    session.clear()

    # If a user submits a photo via POST
    if request.method == "POST":
        # Save a copy of the picture they sent in the current directory
        with open('image.jpg', 'wb') as fh:
            # Get only revelant data, deleting "data:image/png;base64,"
            data = request.data.split(',')[1]
            fh.write(decodestring(data))

        # Load and encode the image
        file = load_image_file('image.jpg')
        encoding = face_encodings(file)

        # Delete our copy of the picture
        remove('image.jpg')

        # If a face was found, find the closest recognized face in the database.
        if encoding:
            distances = face_distance(known_face_encodings, encoding[0])

            # If there is a close match, set name to the name of the recognized user.
            if min(distances) < 0.4:
                match_index = where(distances == min(distances))[0][0]
                session['name'] = known_face_names[match_index]
                # print(name)
                # print(min(distances))
                return "match"
        return "no match"
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def selfie():
    """Upload a picture"""
    # clear user Session
    session.clear()
    
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
            fh.write(decodestring(data))

        # Encode the picture of their face
        file = load_image_file('add.jpg')
        encoding = face_encodings(file)

        # Get rid of our copy of the picture
        remove('add.jpg')

        # If they sent all the required data, add it to the database
        if encoding and firstname and lastname:
            conn = connect('faces.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (name, encoding) VALUES (?, ?)",
                      (username, dumps(encoding)))
            conn.commit()
            conn.close()

            # Add to our working list of encodings
            known_face_encodings.append(encoding[0])
            known_face_names.append(username)
            return "/login"
        else:
            return "error"

    return render_template("register.html")
