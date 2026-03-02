import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Lambda Environment Variables වලින් URL එක ගන්නවා
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Engine එක සහ Session එක හදමු
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB Session එක ගන්න function එක
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
