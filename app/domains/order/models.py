from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.buyer_id", ondelete="CASCADE"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="결제 완료")

    # Relationships
    product = relationship("Product", back_populates="orders")
    buyer = relationship("Buyer", back_populates="orders")
