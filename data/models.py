from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from datetime import datetime

from data.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    interests = Column(String)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Content(Base):

    __tablename__ = "content"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    difficulty = Column(String)
    popularity = Column(Integer)


class Skill(Base):

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class UserSkill(Base):

    __tablename__ = "user_skills"

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )

    proficiency = Column(Float)


class ContentSkill(Base):

    __tablename__ = "content_skills"

    content_id = Column(
        Integer,
        ForeignKey("content.id"),
        primary_key=True
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )


class Interaction(Base):

    __tablename__ = "interactions"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    content_id = Column(
        Integer,
        ForeignKey("content.id")
    )

    type = Column(String)

    rating = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )