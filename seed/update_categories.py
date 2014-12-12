import os
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
	statement_id = Column(Integer, ForeignKey('statement.id'))



engine = create_engine('postgresql://centralbureacracy:centralfiling@localhost/convo')
Session = sessionmaker(bind=engine)

session=Session()

s1=session.query(Statement).get(1)
s1.category='Intro'

s8=session.query(Statement).get(8)
s8.category='Intro'

s33=session.query(Statement).get(33)
s33.category='Intro'

s66=session.query(Statement).get(66)
s66.category='Intro'

s82=session.query(Statement).get(82)
s82.category='Intro'

s129=session.query(Statement).get(120)
s129.category='Intro'

s132=session.query(Statement).get(132)
s132.category='Intro'

s138=session.query(Statement).get(138)
s138.category='Intro'

s146=session.query(Statement).get(146)
s146.category='Intro'

session.commit()

