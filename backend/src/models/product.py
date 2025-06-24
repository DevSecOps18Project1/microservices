"""
SQLAlchemy models for the Product Service API
"""
from sqlalchemy import Column, String, Text, Integer, Double
from db.database import Base

from models.model_base import BaseModel


class Product(BaseModel, Base):
    """Product model."""

    __tablename__ = 'products'

    sku = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Integer, default=0, nullable=False)
    price = Column(Double, default=0, nullable=False)

    def __init__(self, data: dict):
        super().__init__(data.get('name'))
        self.sku = data.get('sku')
        self.description = data.get('description', '')
        self.quantity = data.get('quantity', 0)
        self.price = data.get('price', 0)

    def update(self, data: dict, commit: bool = True) -> bool:
        # Update fields if provided
        for key in ['name', 'sku', 'description', 'quantity', 'price']:
            if key in data:
                setattr(self, key, data[key])
        return super().update(data)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'sku': self.sku,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def get_by_sku(cls, sku):
        return cls.query.filter_by(sku=sku).first()

    @classmethod
    def get_low_quantity(cls, threshold: int):
        return cls.query.filter(cls.quantity < threshold).all()
