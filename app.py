
from flask import Flask, render_template, url_for, request
from flask import g, Markup
from redis import Redis
from Levenshtein import distance
from operator import itemgetter
import random

app = MyServer(__name__)

r = Redis(host='localhost', port=6379)


'''
use Levenshtein distance to find the text most similar to the text the user
just imputted
'''
def closest(inquiry, keys):
  return min([(str(x.id), distance(inquiry, x.text)) for x in keys], key=itemgetter(1))

'''
get and process a response from the sqlalchemy db
input text does not need to be already in the db
'''
def get_comp_response(inquiry):
	keys = r.scan_iter(match='*')
	closest_phrase=closest(inquiry, keys)
	return r.zcard(closest_phrase)


def add_db_user_text(inquiry, user_response):
	#check if user input exists
	elements = r.zscan_iter(inquiry, match=user_response):
	if elements:
		keys = r.scan_iter(match='*')
		for k in keys:
			if k==user_response:
				r.zincby(inquiry, user_response)
				return
		r.zadd(inquiry, 1, user_response)
	else:
		#add user input db
		r.zadd(inquiry, 1, user_response)
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
   app.run(host="0.0.0.0", debug=True)