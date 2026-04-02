from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    sub_id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey("buyers.buyer_id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.seller_id"), nullable=False)

    __table_args__ = (UniqueConstraint('buyer_id', 'seller_id', name='uq_buyer_seller'),)

    buyer = relationship("Buyer", back_populates="subscriptions")
    seller = relationship("Seller", back_populates="followers")

class Wishlist(Base):
    __tablename__ = "wishlists"

    wish_id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey("buyers.buyer_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    buyer = relationship("Buyer", back_populates="wishlists")
    product = relationship("Product", back_populates="in_wishlists")

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey("buyers.buyer_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)

    buyer = relationship("Buyer", back_populates="orders")
    product = relationship("Product", back_populates="orders")
