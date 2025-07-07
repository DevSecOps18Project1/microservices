"""
SQLAlchemy model for RestockLog entity
"""
import logging
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from db.database import Base
from models.model_base import BaseModel

LOG = logging.getLogger(__name__)


class RestockLog(BaseModel, Base):
    """RestockLog model."""

    __tablename__ = 'restock_logs'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True)
    restocked_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, data: dict):
        super().__init__('')
        self.product_id = data.get('product_id')
        self.quantity = data.get('quantity')
        self.reason = data.get('reason')

    def to_dict(self):
        """Convert restock log to dictionary."""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'reason': self.reason,
            'restocked_at': self.restocked_at.isoformat() if self.restocked_at else None
        }

    @classmethod
    def get_by_product_id(cls, id_: int):
        restock_log = cls.query.filter(cls.product_id == id_).all()  # pylint: disable=E1101
        return restock_log
