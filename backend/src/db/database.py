"""
Database connection handling for the User Service API
"""
import logging
from time import sleep
import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from my_config.config import Config

MAX_RETRIES = 10
RETRY_DELAY = 2

# Create engine
url = Config.get_url()
logging.info(f'Set DB in URL : {url}')
engine = create_engine(url)

# Create scoped session
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Create declarative base
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Initialize the database."""
    sleep(RETRY_DELAY)

    for attempt in range(1, MAX_RETRIES + 1):
        logging.info(f'Attempt {attempt} of {MAX_RETRIES} to create database tables...')
        try:
            # Import models here to ensure they are registered properly on the metadata
            from models.user import User  # pylint: disable=C0415,W0611,R0401
            from models.product import Product  # pylint: disable=C0415,W0611,R0401
            from models.restock_log import RestockLog  # pylint: disable=C0415,W0611,R0401

            Base.metadata.create_all(bind=engine)
            logging.info('Database tables created successfully!')
            break  # Exit the loop if successful
        except sqlalchemy.exc.OperationalError as e:
            logging.error(f'Error creating tables: {e}')
            if attempt < MAX_RETRIES:
                logging.info(f'Retrying in {RETRY_DELAY} seconds...')
                sleep(RETRY_DELAY)
            else:
                logging.info('Maximum retry attempts reached. Could not create database tables.')
