# infra.py is responsible for setting up the database connection and creating the session factory.
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env file
load_dotenv()

# Define the database connection URL
db_url = os.getenv("DB_URL")

if not db_url:
    raise ValueError("DB_URL environment variable is not set")

# Create the SQLAlchemy engine
engine = create_engine(db_url)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()