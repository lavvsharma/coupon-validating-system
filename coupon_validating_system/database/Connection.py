"""
Author: Lav Sharma
Created on: 5th Dec 2023
"""

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import coupon_validating_system.configuration as config
from coupon_validating_system.ModuleLogger import setup_logger

logger = setup_logger()

try:
    # ========================================================================
    # Create database connection using sqlalchemy
    # ========================================================================
    engine = create_engine(f'mysql+mysqlconnector://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}'
                           f'@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}',
                           pool_pre_ping=True)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

except exc.SQLAlchemyError as sql_alchemy_error:
    raise Exception('Failed to connect to the database.')

except Exception as error:
    logger.error('Error in connecting to database or in creating session_object' +
                 f'\nException - {str(error)}', exc_info=True)
