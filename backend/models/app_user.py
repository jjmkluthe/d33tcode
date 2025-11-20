from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class AppUser(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    email_address = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False, default="standard")
    update_password = Column(Boolean, default=True)

    submissions = relationship("Submission", back_populates="app_user", cascade="all, delete-orphan")