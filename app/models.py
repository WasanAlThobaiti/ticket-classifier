from sqlalchemy import Column, String, DateTime, Text, Integer
from datetime import datetime
from app.database import Base

class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, classified, failed
    category = Column(String, nullable=True)     # billing, technical, account, other
    priority = Column(String, nullable=True)     # low, medium, high
    summary = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)