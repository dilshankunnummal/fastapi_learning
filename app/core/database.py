from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:121212@localhost:5432/dilshan"
engine = create_engine(db_url)
#sessionmaker is use to create session, everthing in databsae is sesion 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # engine use to help to connect db