from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy import event, DDL

Base = declarative_base()


# User table class
class User(Base):
    # Set table name
    __tablename__ = 'user'

    # Map table columns
    name = Column(String(20), nullable=False)
    picture = Column(String(250), nullable=True)
    email = Column(String(250), nullable=False)
    id = Column(Integer, nullable=False, primary_key=True)


# Restaurant table class
class Restaurant(Base):
    # Set table name
    __tablename__ = 'restaurant'

    # Map table columns
    name = Column(String(20), nullable=False)
    description = Column(String(), nullable=False)
    telephone = Column(String(20), nullable=False)
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description,
            'telephone': self.tel,
            'id': self.id,
            'user id': self.user_id,
        }


# MenuItem table class
class MenuItem(Base):
    # Set table name
    __tablename__ = 'menuItem'

    # Map table columns
    name = Column(String(20), nullable=False)
    description = Column(String(), nullable=False)
    category = Column(String(20), nullable=False)
    price = Column(String(8), nullable=False)
    id = Column(Integer, nullable=False, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant, backref=backref(
        "menuItem", cascade="all, delete"))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'id': self.id,
            'restaurant id': self.restaurant_id,
            'user id': self.user_id,
        }


engine = create_engine('sqlite:///restaurantmenu.db')
# Add classes as tables to the 'restaurantmenu.db' database
Base.metadata.create_all(engine)
