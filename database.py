import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class ShortLink(Base):
    """The shortLink table"""
    __tablename__ = 'shortLink'
    slug = Column(String(250), primary_key=True)
    destination = Column(String(2083), nullable=False)
    @property
    def serialize(self):
        """creates JSON object for api endpoint"""
        return {
            'slug': self.name,
            'destination': self.destination
        }

##on running of this file, db is generated. View with DB Browser
engine = create_engine('sqlite:///smallernatordb.db')

Base.metadata.create_all(engine)