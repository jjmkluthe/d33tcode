from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Submission(Base):
    __tablename__ = "submission"

    app_user_id = Column(
        Integer,
        ForeignKey("app_user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    project_id = Column(
        Integer,
        ForeignKey("project.id", ondelete="CASCADE"),
        primary_key=True,
    )
    is_complete = Column(Boolean, nullable=False, default=False)
    grade = Column(Numeric(5, 2), nullable=True)

    app_user = relationship("AppUser", back_populates="submissions")
    project = relationship("Project", back_populates="submissions")