
from flask import Flask, render_template, url_for, request
from flask import g, Markup
from flask.ext.sqlalchemy import SQLAlchemy
from Levenshtein import distance
from operator import itemgetter

class MyServer(Flask):

    def __init__(self, *args, **kwargs):
            super(MyServer, self).__init__(*args, **kwargs)

            #instanciate your variables here
            self.computer_tscrpt = []
            self.user_tscrpt = []

app = MyServer(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://centralbureacracy:centralfiling@localhost/convo'
db = SQLAlchemy(app)

'''
updated to many-to-many relationship
'''
node_to_node = db.Table("node_to_node", 
    db.Column("statement_id", db.Integer, db.ForeignKey("node.id"), primary_key=True),
    db.Column("response_id", db.Integer, db.ForeignKey("node.id"), primary_key=True),
    db.Column("weight", db.Float)
)

class Node(db.Model):
	__tablename__ = 'node'
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(500))
	freq = db.Column(db.Float)
	response_nodes = db.relationship("Node",
						secondary=node_to_node,
						primaryjoin=id==node_to_node.c.statement_id,
						secondaryjoin=id==node_to_node.c.response_id,
						backref="statement_nodes")

'''
use Levenshtein distance to find the text most similar to the text the user
just imputted
'''
def closest(words, lst):
    return min([(str(x.id), distance(words, x.text)) for x in lst], key=itemgetter(1))

'''
get and process a response from the sqlalchemy db
input text does not need to be already in the db
'''
def get_comp_response(words):
	s=Node.query.all()
	c=closest(words, s)
	print c
	n=Node.query.filter(Node.id==int(c[0])).first()
	return n.response_nodes[0]	#return the response
	

def add_db_user_text(words, previous_words):
	#check if user input exists
	ur=Node.query.filter(Node.text.ilike(words)).first()
	if ur:
		#check if there is a connection between user input and statement
		ps=Node.query.filter(Node.text.ilike(previous_words)).first()
		if ur.id!=ps.response_nodes[0].id:
			ps.response_nodes.append(ur)
			db.session.commit()
	else:
		#add user input to Node table
		r=Node(text=words, freq=0)
		db.session.add(r)
		db.session.commit()
		#link user input to response and parent statement
		ps=Node.query.filter(Node.text.ilike(previous_words)).first()
		ps.response_nodes.append(r)
		db.session.add(ps)
		db.session.commit()
	return

#main app
@app.route('/', methods=['POST', 'GET'])
def index ():

	if app.computer_tscrpt==[]:
		app.computer_tscrpt.append('Hello!')

	if request.method == 'POST':
		if request.form['submit'] == 'talk':

			# login and validate the user...
			user_input=request.form['user_input']

			#add user input to user message transcript array
			app.user_tscrpt.append(user_input)

			#get an appropriate response and add it to the computer
			#message transcript array
			cr= get_comp_response(user_input)
			app.computer_tscrpt.append(cr.text)

			#save user input to the database
			add_db_user_text(user_input, app.computer_tscrpt[-1])

		else:
			app.computer_tscrpt=[]
			app.user_tscrpt=[]


	return render_template('index.html', 
							computer_tscrpt=app.computer_tscrpt, 
							user_tscrpt=app.user_tscrpt)


if __name__ == '__main__':
	app.debug=True
	app.run(port=5000)