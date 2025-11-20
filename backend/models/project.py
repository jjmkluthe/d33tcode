from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from .base import Base

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    problem_id = Column(Integer, ForeignKey("problem.id", ondelete="RESTRICT"), nullable=True)
    solution_id = Column(Integer, ForeignKey("solution.id", ondelete="RESTRICT"), nullable=True)
    difficulty = Column(Integer, nullable=True)

    problem = relationship("Problem", back_populates="projects")
    solution = relationship("Solution", back_populates="projects")
    videos = relationship("Video", back_populates="project")

    submissions = relationship(
        "Submission",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint("difficulty BETWEEN 1 AND 5", name="ck_project_difficulty"),
    )