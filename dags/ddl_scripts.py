from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from constants import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

def create_car_listings_table():
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    session.close()
