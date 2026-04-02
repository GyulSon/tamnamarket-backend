from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("sellers.seller_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100))
    category = Column(String(50))
    weight = Column(String(50))
    harvest_date = Column(Date)
    taste_feature = Column(Text)
    farmer_comment = Column(Text)
    price = Column(Integer)
    voice_path = Column(String(255))
    final_description = Column(Text)
    is_selling = Column(Boolean, default=True)

    # Relationships
    seller = relationship("Seller", back_populates="products")
    images = relationship("ProductImage", back_populates="product", uselist=False, cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="product")
    in_wishlists = relationship("Wishlist", back_populates="product")

class ProductImage(Base):
    __tablename__ = "product_images"

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)
    img1 = Column(String(255))
    img2 = Column(String(255))
    img3 = Column(String(255))
    img4 = Column(String(255))

    product = relationship("Product", back_populates="images")

class Wishlist(Base):
    __tablename__ = "wishlists"

    wishlist_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.buyer_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="in_wishlists")
    buyer = relationship("Buyer", back_populates="wishlists")
