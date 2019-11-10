from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from api import Base


class Items(Base):
    __tablename__ = 'items'

    id_ = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)


class Stock(Base):
    __tablename__ = 'stock'

    id_ = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id_"), nullable=False)
    qty = Column(Integer, nullable=False)
    retail_price = Column(Float(precision=2), nullable=False)
    wholesale_price = Column(Float(precision=2), nullable=False)
    discount = Column(Float(precision=2))
    mfd_date = Column(DateTime, nullable=False)
    exp_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    item = relationship("Items", backref="payments", uselist=False , lazy='subquery')


