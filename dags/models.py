from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Define the base class
Base = declarative_base()

# Define the CarListing model
class CarListing(Base):
    __tablename__ = 'car_listings'
    
    # articleID from link
    id = Column(Integer, primary_key=True)  
    title = Column(String, nullable=False)
    price = Column(Float)
    link = Column(String(35), nullable=False)

    def __init__(self, id, title, price, link):
        self.id = id
        self.title = title
        self.price = price
        self.link = link

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'link': self.link
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            title=data['title'],
            price=data['price'],
            link=data['link']
        )