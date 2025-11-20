from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Solution(Base):
    __tablename__ = "solution"

    id = Column(Integer, primary_key=True, index=True)
    git_link = Column(String(255), nullable=False)
    solution_description = Column(Text, nullable=False)

    projects = relationship("Project", back_populates="solution")