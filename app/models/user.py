from sqlalchemy import Column, Integer, String, Enum as SAEnum
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.viewer)
    status = Column(SAEnum(UserStatus), nullable=False, default=UserStatus.active)
