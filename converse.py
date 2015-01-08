import os
import nltk
import sqlalchemy
#import app
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, or_
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from sklearn import svm
from Levenshtein import distance
from operator import itemgetter

Base = declarative_base()


class Statement(Base):
	__tablename__='statement'
	id = Column(Integer, primary_key=True)
	text = Column(String(500))
	freq = Column(Float)
	children = relationship("Response", backref="statement", lazy="dynamic")


class Response(Base):
	__tablename__='response'
	id =Column(Integer, primary_key=True)
	text = Column(String(500))
	statement_id=Column(Integer)
	parent_id = Column(Integer, ForeignKey('statement.id'))

def closest(words, lst):
    #return min([(x, distance(word, x)) for x in lst], key=itemgetter(1))
    return min([(str(x.id), distance(words, str(x.text))) for x in lst], key=itemgetter(1))

def get_response(words):
	s=Statement.query.filter(Statement.text.ilike(words)).all()
	c=closest(words, s)
	r = Response.query.filter(Response.parent_id==int(c[0])).first()
	return r.text

engine = create_engine('postgresql://centralbureacracy:centralfiling@localhost/convo')
Session = sessionmaker(bind=engine)

session=Session()

q=[]
labels=[]
ns=[]
i=0
s=session.query(Statement).filter(Statement.text.ilike('hey%')).all()
for k in s:
	q.append(str(k.text))
c=closest("Hey", s)

print int(c[0])
r = session.query(Response).filter(Response.statement_id==int(c[0])).first()
#
print r.text
'''

print get_response('Hey')