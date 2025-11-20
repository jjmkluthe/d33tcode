from sqlalchemy import Column, Integer, String, Text, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("project.id"),
        nullable=False,
    )
    yt_code = Column(String(32), nullable=False)
    type = Column(String(16), nullable=True)
    ordinal = Column(Integer, nullable=True)

    project = relationship("Project", back_populates="videos")

    __table_args__ = (
        CheckConstraint(
            "type IN ('intro','tutorial','solution')",
            name="ck_video_type",
        ),
    )