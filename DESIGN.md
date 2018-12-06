# Design
## The goal
Our goal was to make a proof-of-concept facial recognition login page for Harvard. This consists of 3 pages:

* A login page
* A register page
* And a welcome page

The login page contains a webcam element where users can take a pictures of themselves. If their picture matches a face within our database of faces they get redirected to the welcome page, which recognizes them by name. The registration page contains a from and a webcam element. Users must fill out the form and submit a picture of themselves to register their face and add it to the database. Our pages mirror Harvard's website and we populated our database with faces of Harvard students.

## Pseudocode
```
Login page:
  Show webcam selfie tool
  When user takes picture:
    Send picture to server:
      If server recognizes known user in picture:
        Identify user's name
        Redirect to welcome page
      Else:
        Tell user they were not recognized
  When user clicks link to register page:
    Redirect to the register page

Register page:
  Show webcam selfie tool, name form
  When user clicks "register" button:
    If user has filled out form and taken picture with face:
      Add user's name and face to database
      Redirect to login page
    Else:
      Show error

Welcome page:
  Welcome user by name
  Log user out
```

## Implementation
We decided that we would be able to implement our project using what we learned in CS50, specifically SQLite, Flask, Python, JavaScript, Jinja, HTML and CSS. In our research phase, we identified all the pieces we would need to implement our plans. We found an open-source facial recognition library for Python on GitHub (https://github.com/ageitgey/face_recognition) and a tutorial with source code on taking pictures via webcam (https://tutorialzine.com/2016/07/take-a-selfie-with-js).

At first we tried to install face_recognition on the CS50 IDE, but ran into error installing one of its dependencies, dlib. The library installed fine on our personal machines, so we decided to make a private GitHub repository and store our project there. This required that we learn Git.

We set up a Flask web app and organized our project accordingly.

### Database

We created a database of Harvard students and their faces.

We used the Harvard Facebook and scraped all the images and their corresponding names. Using https://www.webscraper.io/, we got a csv document with a name column and the name of the image column (because the name of the image is hashed). Then, using Fatkun Batch Download Image, a Chrome extension, we downloaded a folder "students" containing the images of every student. The name of the images in that folder are hashed and needed to be changed. For that, we wrote filename_changer.py to change the hashed name with their real name using the csv file containing both values.

We wrote dbmaker.py to create a database with each face's encodings and names. Dbmaker.py takes .jpg images from a folder called "students" in the same directory and puts them in a database with their face encodings and names.

| id   | name               | encoding |
| ---- | ------------------ | -------- |
| 1    | Finlayson, Matthew | ####     |
| 2 | Gao, Mary | #### |
| 3 | Michalak, Winston | #### |


### Login

The login page is modified from the Harvard Key login page, but we replaced the central element containing the login form with a webcam and a "take picture" button. When the user clicks this button, it saves a frame from the webcam and sends it via a XML HTTP request to the server. On the server, we use the face_recognition library to compare the face to the list of known faces. If there is a close match, the user is sent to the welcome page where they are greeted by name. Choosing the minimum threshold of resemblance was a major consideration. For our project presentation, we wanted the server to be able to recognize most Harvard students' faces from their sometimes inaccurate and low resolution ID photos without forcing to register their faces, so we set the threshold relatively low, that is, the server is more likely to accept questionable faces. The drawback of this approach is that misidentification is more common, especially with non-white faces. This somewhat racist bias is a common problem with facial recognition technologies.

When the user's face is recognized, it is saved as a global variable `name` in app.py. This is bad design.

### Register

The register page was challenging because we had to combine a form with our picture taking. We resolved this by creating a `FormData` object in JavaScript and appending it to include the image before submitting it via an XML HTTP request. We also used server-side validation to require that the picture have a face in it and the form have a first and last name. We did not have a way to make sure that each user is unique because we do not have access to students' ID numbers, so we decided to register all faces and names as new users. This makes our project accessible to non-Harvard students because anyone anyone can register their name and face. The drawback is that we cannot update an existing user's face encoding.

### Welcome

We used Jinja to welome users by name when they log in. We took a screenshot of the my.harvard page to act as a fun background. We decided to do this instead of taking its source code because the source code had many links to multiple other css, Javscript files. We added invisible buttons around the logo on the top left corner and the sign out in the top right corner which redirects the user to login. We also added a log out button to make it more obvious. We decided to log the user back out immediately when loading the page so that a simple refresh will bring the user back to the login page.





*A "design document" for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. Your design document should be at least several paragraphs in length. Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff a technical tour of your project underneath its hood.*
