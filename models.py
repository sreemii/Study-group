from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Enum
from sqlalchemy.orm import relationship
from base import Base
import datetime
import enum
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
   

    groups = relationship("GroupMember", back_populates="user", cascade="all, delete")

class StudyGroup(Base):
    __tablename__ = "study_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)

    members = relationship("GroupMember", back_populates="group", cascade="all, delete")
    sessions = relationship("StudySession", back_populates="group", cascade="all, delete")
    resources = relationship("Resource", back_populates="group", cascade="all, delete")

class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey("study_groups.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="groups")
    group = relationship("StudyGroup", back_populates="members")

class StudySession(Base):  # ✅ Correct name
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id", ondelete="CASCADE"))
    scheduled_time = Column(DateTime, default=datetime.datetime.utcnow)
    
    group = relationship("StudyGroup", back_populates="sessions")

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)

    group = relationship("StudyGroup", back_populates="resources")
