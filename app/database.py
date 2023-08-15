from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
import config
# Corrected database URL without @ in the password
password = config.settings.database_password
password_encoded = urllib.parse.quote(password, safe='')
SQLALCHEMY_DATABASE_URL = f'postgresql://{config.settings.database_username}:{password_encoded}@{config.settings.database_hostname}:{config.settings.database_port}/{config.settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Use keyword arguments for autocommit and autoflush
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='das@2001',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was succefull!")
        break
    except Exception as error:
        print("Connecting to databse Falid")
        print("Error: ",error)
        time.sleep(3)'''