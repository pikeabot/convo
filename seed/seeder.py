import os
from os import listdir
from os.path import isfile, join

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from flask.ext.sqlalchemy import SQLAlchemy

Base = declarative_base()


class Statement(Base):
	__tablename__='statement'
	id = Column(Integer, primary_key=True)
	text = Column(String(500))
	freq = Column(Float)
	category = Column(String(50))
	children = relationship("Response", backref="statement", lazy="dynamic")

class Response(Base):
	__tablename__='response'
	id =Column(Integer, primary_key=True)
	text = Column(String(500))
	statement_id=Column(Integer)
	parent_id = Column(Integer, ForeignKey('statement.id'))

dir_list=os.listdir(os.getcwd()+'/data')
#filename='convo1.txt'
#filename='reddit1.txt'
#filename='reddit2.txt'
#filename='reddit3.txt'
#filename='reddit4.txt'
#filename='reddit5.txt'
#filename='reddit6.txt'
#filename='reddit7.txt'
#filename='reddit8.txt'
#filename='reddit9.txt'


for filename in dir_list: 
	try:
		fh=open(os.getcwd()+'/data/'+filename, "r")


	except IOError:
			print "Error: can\'t find file or read data"
	else:
		engine = create_engine('postgresql://centralbureacracy:centralfiling@localhost/convo')
		Session = sessionmaker(bind=engine)

		session=Session()

		#lines=[]
		lines=fh.readlines()
		
		for line in lines:
			if line[0]!='#':
				session.add(Statement(text=line.strip(), freq = 0, category='Core'))
		session.commit()
		
		for i in range(0, len(lines)-1):
			if lines[i][0]!='#':
				s=session.query(Statement).filter_by(text=lines[i].strip()).first()
				rs=session.query(Statement).filter_by(text=lines[i+1].strip()).first()
				r=Response(text=lines[i+1].strip(), statement_id=rs.id, parent_id=s.id) 
				s.children.append(r)
				session.add(s)
				session.add(r)

		session.commit()
		
		fh.close()
