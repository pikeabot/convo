import os
from os import listdir
from os.path import isfile, join

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from flask.ext.sqlalchemy import SQLAlchemy

Base = declarative_base()

node_to_node = Table("node_to_node", Base.metadata,
    Column("statement_id", Integer, ForeignKey("node.id"), primary_key=True),
    Column("response_id", Integer, ForeignKey("node.id"), primary_key=True),
    Column("weight", Float)
)

class Node(Base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    freq = Column(Float)
    response_nodes = relationship("Node",
                        secondary=node_to_node,
                        primaryjoin=id==node_to_node.c.statement_id,
                        secondaryjoin=id==node_to_node.c.response_id,
                        backref="statement_nodes"
    )


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
		
		#add all lines to the db
		for line in lines:
			if line[0]!='#':
				#session.add(Statement(text=line.strip(), freq = 0, category='Core'))
				session.add(Node(text=line.strip(), freq = 0))
		session.commit()
	

		#create table linking statements with responses
		for i in range(0, len(lines)-1):
			if lines[i][0]!='#' :
				
				s=session.query(Node).filter_by(text=lines[i].strip()).first() 	#statement
				r=session.query(Node).filter_by(text=lines[i+1].strip()).first() #response
				s.response_nodes.append(r)
				session.add(s)

		session.commit()
		
		fh.close()
