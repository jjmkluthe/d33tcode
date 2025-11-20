from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Problem(Base):
    __tablename__ = "problem"

    id = Column(Integer, primary_key=True, index=True)
    git_link = Column(String(255), nullable=False)
    problem_description = Column(Text, nullable=True)

    projects = relationship("Project", back_populates="problem")