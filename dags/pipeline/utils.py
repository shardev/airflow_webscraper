import csv
import pandas as pd
import ast
from models import CarListing


def create_csv(listings, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for listing in listings:
            writer.writerow({'Title': listing.title, 'Price': listing.price, 'Link': listing.link})


def read_csv_and_build_car_listings(csv_filename):
    df = pd.read_csv(csv_filename)
    
    listings = []
    for index, row in df.iterrows():
        title = row['Title']
        price = row['Price']
        link = row['Link']
        
        listing = CarListing(int(link.split('/')[-1]),title, price, link)
        listings.append(listing)
    
    # Serialize before sending to X-COM
    return [car.to_dict() for car in listings] 
    


def data_cleansing(car_listings):
    # From string to list of dicts
    car_listings = ast.literal_eval(car_listings)
    
    # Deserialize from dict to list of CarListing objects
    car_listings_obj = [CarListing.from_dict(data) for data in car_listings]
    
    # Format prices for non string price listings
    for listing in car_listings_obj:
        if listing.price != 'Na upit':
           listing.price = int(''.join(filter(str.isdigit, listing.price))) 
        else:
            listing.price = None

    # Serialize before sending to X-COM
    return [car.to_dict() for car in car_listings_obj] 
    
    