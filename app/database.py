from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setings
SQLALCHEMY_DATABASE_URL = f"postgresql://{setings.database_username}:{setings.database_password}@{setings.database_hostname}:{setings.database_port}/{setings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# try:
#     con = psycopg2.connect(host='localhost',database='FastApi',user='postgres',password=password,cursor_factory=RealDictCursor)
#     cursor = con.cursor()
#     print("DataBase Connection Has Succesfuly")
# except Exception as error:
#     print("Failed Connect To Database")
#     print("Error :",error)