import os, sys, logging
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database


LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }

if len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)

database_uri='postgresql://{0}:{1}@localhost/convo'.format(sys.argv[1], sys.argv[2])

#check if database exists and if not create database convo
if not database_exists(database_uri):
    print 'Database convo does not exist'
    print 'Creating database convo'
    create_database(database_uri)
    print 'Database convo created'

#connect to sqlalchemy engine
engine = create_engine('postgresql://train:kaggle@localhost/convo')
Session = sessionmaker(bind=engine)
session=Session()

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

#create tables Node and node_to_node
Base.metadata.create_all(engine, checkfirst=True)