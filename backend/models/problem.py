from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Problem(Base):
    __tablename__ = "problem"

    id = Column(Integer, primary_key=True, index=True)
    git_link = Column(String(255), nullable=False)
    problem_description = Column(Text, nullable=True)

    projects = relationship("Project", back_populates="problem")