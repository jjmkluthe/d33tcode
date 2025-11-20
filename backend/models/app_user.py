from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class AppUser(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    email_address = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False, default="standard")
    update_password = Column(Boolean, default=True)

    submissions = relationship("Submission", back_populates="app_user", cascade="all, delete-orphan")