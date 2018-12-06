# web-face-authentication

## Motivation
The goal of the project was to create a proof-of-concept for website-based facial
authentication. This demo is of a mock HarvardKey login page. Using the computer's
webcam, a photo is taken and matched against the Harvard students database (school
 year 2018-2019). If a match is found, the user "logs into" my.harvard.edu. A
 user can also register a new photo if they are not already in the database.

## Requirements

See requirements.txt for full list of requirements



* Face Recognition
  * Mac or Linux:
    * Install dlib
      - https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf
    * `pip install face_recognition`
  * Windows: (not officially supported)
    * https://github.com/ageitgey/face_recognition/issues/175#issue-257710508
  * Other
    * See README.md from https://github.com/ageitgey/face_recognition
* Flask
  * `pip install Flask`

## Credits

*Documentation for your project in the form of a Markdown file called `README.md`. This documentation is to be a user’s manual for your project. Though the structure of your documentation is entirely up to you, it should be incredibly clear to the staff how and where, if applicable, to compile, configure, and use your project. Your documentation should be at least several paragraphs in length. It should not be necessary for us to contact you with questions regarding your project after its submission. Hold our hand with this documentation; be sure to answer in your documentation any questions that you think we might have while testing your work.*
