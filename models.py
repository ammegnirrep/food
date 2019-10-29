from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class CupboardItem(Base):
    __tablename__ = 'cupboard_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    quantity = Column(Integer)
    expiry_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name =None, quantity= None, expiry_date=None):
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date

    def __repr__(self):
        return '<CupboardItem %r>' % (self.name)
