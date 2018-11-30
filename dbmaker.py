# Takes .jpg images from a folder called "students" in the same directory
# and puts them in a database with their face encodings and names
import face_recognition
import os
import sqlite3
import pickle

conn = sqlite3.connect('faces.db')
c = conn.cursor()

files = os.listdir('students')

if '.DS_Store' in files:
    files.remove('.DS_Store')

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

for file in files:
    image = face_recognition.load_image_file('directory/' + file)
    encoding = face_recognition.face_encodings(image)
    known_face_encodings.append(encoding)
    name = file.replace('.jpg','')
    known_face_names.append(file.replace('.jpg',''))
    c.execute("INSERT INTO users (name, encoding) VALUES (?,?)",
              (name, pickle.dumps(encoding)))

print(known_face_encodings[5])
conn.commit()

# c.execute("SELECT encoding FROM users WHERE name = 'Finlayson, Matthew'")
# c.execute("SELECT encoding FROM users")
# dpickle = c.fetchone()
# print(pickle.loads(dpickle[0]))
# print(dpickle[0])

conn.close()
