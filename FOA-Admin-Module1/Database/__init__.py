"""
Description : Creating a Database, Configuring Session.
"""

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

# Connect to Postgresql
db_url = os.getenv("LOCAL_DATABASE_URL")

# An Engine, which the Session will use for connection
engine = create_engine(db_url, echo = False)

# Create Database (admin_module) if not exist
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))

# Base class stores a catlog of classes and mapped tables in the Declarative system.
Base = declarative_base()

# create a configured "Session" class
local_session = sessionmaker(autocommit = False, autoflush= False, bind=engine)
Session = scoped_session(local_session)

