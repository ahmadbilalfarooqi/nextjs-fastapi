# database.py

import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
_:bool = load_dotenv(find_dotenv())
key = os.environ.get("SQLALCHEMY_DATABASE_URL")
engine = create_engine(key)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
Base = declarative_base()
