import ast
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, CarListing
from constants import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

def delta_insert(new_car_listings):
    # Fetch current car_listings from db
    engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    current_car_listings = session.query(CarListing).all()

    # From string to list of dicts => then to CarListing object
    new_car_listings = ast.literal_eval(new_car_listings)
    new_car_listings = [CarListing.from_dict(data) for data in new_car_listings]
    
    # Find difference between new and current car listings
    delta_update_entries = []
    for new_car_listing in new_car_listings:
        if not any(new_car_listing.link == current_car_listing.link for current_car_listing in current_car_listings):
            delta_update_entries.append(CarListing(int(new_car_listing.link.split('/')[-1]), new_car_listing.title, new_car_listing.price, new_car_listing.link))
            

    # Insert delta
    session.add_all(delta_update_entries)
    session.commit()
    session.close()
    
    # Return list of dicts
    return [car.to_dict() for car in delta_update_entries] 
    