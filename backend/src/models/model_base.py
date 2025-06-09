"""
SQLAlchemy models for the Base Model
"""
import logging
import uuid

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.exc import IntegrityError
from db.database import db_session


class BaseModel:
    """Base model."""

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        raise NotImplementedError(f'Please implement fhe function for {self.__class__.__name__}')

    def create(self, commit=True) -> bool:
        try:
            db_session.add(self)
            if commit:
                db_session.commit()
            return True
        except IntegrityError as e:
            logging.exception(f'create : unexpected exception : {e}')
            db_session.rollback()
            return False
        except Exception as e:  # pylint: disable=W0718
            logging.exception(f'create : unexpected exception : {e}')
            db_session.rollback()
            raise e

    def update(self, _: dict, commit=True) -> bool:
        try:
            if commit:
                db_session.commit()
            return True
        except IntegrityError:
            db_session.rollback()
            return False
        except Exception as e:  # pylint: disable=W0718
            logging.exception(f'update : unexpected exception : {e}')
            db_session.rollback()
            raise e

    def delete(self, commit=True):
        try:
            db_session.delete(self)
            if commit:
                db_session.commit()
        except Exception as e:  # pylint: disable=W0718
            logging.exception(f'delete : unexpected exception : {e}')
            db_session.rollback()
            raise e

    @classmethod
    def get_by_id(cls, id_: int):
        user = cls.query.filter(cls.id == id_).first()  # pylint: disable=E1101
        return user

    @classmethod
    def get_by_uuid(cls, uuid_: int):
        user = cls.query.filter(cls.uuid == uuid_).first()  # pylint: disable=E1101
        return user

    @classmethod
    def get_all(cls) -> list:
        user_list = cls.query.order_by(cls.created_at.asc()).all()  # pylint: disable=E1101
        return user_list

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name} (ID: {self.id})>'
