import logging

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger('db_connection')

if config('TEST_MODE', default=False, cast=bool):
    DB_URL = config('DB_URL_TEST')
else:
    DB_URL = config('DB_URL')

logger.info(DB_URL)
engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
