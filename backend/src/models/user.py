"""
SQLAlchemy models for the User Service API
"""
from sqlalchemy import Column, String
from db.database import Base

from models.model_base import BaseModel


class User(BaseModel, Base):
    """User model."""

    __tablename__ = 'users'

    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)

    def __init__(self, data: dict):
        super().__init__(data.get('name'))
        self.email = data.get('email')
        self.phone = data.get('phone')

    def update(self, data: dict, commit: bool = True) -> bool:
        # Update fields if provided
        for key in ['name', 'email', 'phone']:
            if key in data:
                setattr(self, key, data[key])
        return super().update(data)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            # 'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }
