#Introduction

Attempt at writing a virtual chat program where the other person is the computer. Intended to be a flirting trainer for friends so they could practice talking to women in a safe, no pressure environment. Database was seeded using text conversations from the subreddit -TextTranscripts. Highly recommended reading. 

#Install

##Requirements:

* Python 2.7
* Postgresql
* SQLAlchemy
* Flask
* [SQLalchemy-utils](https://sqlalchemy-utils.readthedocs.org/en/latest/#)
* python-levenshtein<br>
        **sudo apt-get install python-Levenshtein**

##Create the database and tables:

In Postgresql, set up a user and password with superuser privileges

###To setup the postgresql database:
   python seed/setup_db.py username password

###To seed the database:
   python seed/seeder.py

#Run 
Run python app.py from command line. 


