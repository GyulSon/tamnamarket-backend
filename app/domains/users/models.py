from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Seller(Base):
    __tablename__ = "sellers"

    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    residence = Column(String(100))
    experience = Column(Text)
    repurchase_rate = Column(Numeric(5, 2))
    total_sales = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    images = relationship("SellerImage", back_populates="seller", uselist=False, cascade="all, delete-orphan")
    products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")
    followers = relationship("Subscription", back_populates="seller")

class SellerImage(Base):
    __tablename__ = "seller_images"

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("sellers.seller_id", ondelete="CASCADE"), nullable=False)
    img1 = Column(String(255))
    img2 = Column(String(255))
    img3 = Column(String(255))
    img4 = Column(String(255))

    seller = relationship("Seller", back_populates="images")

class Buyer(Base):
    __tablename__ = "buyers"

    buyer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="buyer")
    wishlists = relationship("Wishlist", back_populates="buyer")
    orders = relationship("Order", back_populates="buyer")
