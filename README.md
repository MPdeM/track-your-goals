# GOAL TRACKING V1.0

V 1.0 :initial release of a web application to track project goals.

The goal of this project is create web application using Flask to track goals using login functionality.

Flask web aplication distribuyion code:

  - application.py (or app.py) contains the python code controling the application
  - requirements.txt contains a list of all libraries
  - goals.db contains the SQL tables users and goals (sqlite3 in this case)
  - statics/ folder with all static code like styles.css and images
  - templates/ folder with the different routes .html


One of the common design patters is MVC - Model View Controller -
    - Model: contains the application data (sql database)
    - View: presents the model data to the user ( the html pages)
    - Controller: the piece connecting view and model (the application.py)

  ![Prof David Malan CS50 Harvard](statics/images/MVC_DesignPatern.png)

I used CD50 IDE. It will only required instalation and it can be runned on your local host http://localhost:8080/.

## Run flask application

In this applcation, I am using "GET" and "POST", and templates like layout.html and it was written following Prof Malan lecture (CS50 Lecture9 Flask).

![run flask application](statics/images/image1.png)
 
 First I will need to register because I am a new user
 
 ![directed to /register ](statics/images/image3.png)
 
 Once register I can add the goals by going to Add Goals
 
![goals added are displayed on the main page ](statics/images/image5.png)
![goals added are displayed on the main page ](statics/images/image6.png)

Goals can be modified and marked as done or erased in similar way. This will modify the goals dataset accordingly.

![goals marked as complited](statics/images/image7.png)

Errors are accounted accordingly as in this case after trying to log in with an incorrect password. 
![goals marked as complited](statics/images/image8.png)

## Important Security Considerations 
The passwords from the users are hashed before to be saved using werkzeug. No password is never directly stored 
To ensure privacy of the data the application uses POST requests.
## Conclusions

This is a first version but I learned:
  - the importance of handling security issues. how to hash passwords prior to saving in the database and how to use POST request to ensure privacy.
  - the importance of reporting user errors that can be easily recogniced. 
  - web application design using Bootstrap
  - debugging
  - debugging
  - start AND finish a working product
  - 
I totally enjoyed this V1.0 an I will have loved to have more time. V1.1 will be comming but not part of this subbmission.

Thanks to Prof David Malan, Brian Yu and Doug Lloyd and to everybody else that made CS50 possible.
 