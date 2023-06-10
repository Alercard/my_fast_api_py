import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# echo=True means that the engine will log all the SQL it executes to the terminal
engine = create_engine(database_url, echo=True)

# sessionmaker is a factory for making sessions
Session = sessionmaker(bind=engine)

# declarative_base is a factory for creating base classes for our models
# helps to manage the relationship between our models and the database
Base = declarative_base()
