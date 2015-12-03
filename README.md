Attempt at writing a virtual chat program where the other person is the computer. Intended to be a flirting trainer for friends so they could practice talking to women in a safe, no pressure environment. Database was seeded using text conversations from the subreddit -TextTranscripts. Highly recommended reading. 

Uses Flask, SQLAlchemy, SQLalchemy-utils and PostgreSQL. 

To create the datbase and tables:
To setup the postgresql database run python app.py username password
*assumes that you have postgresql and a user with superuser permissions set up already

Run python seeder.py to seed the database.

Run python app.py from command line. 


