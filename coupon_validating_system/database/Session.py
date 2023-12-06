"""
Author: Lav Sharma
Created on: 5th Dec 2023
"""

from contextlib import contextmanager

from coupon_validating_system.database.Connection import SessionLocal


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        # ========================================================================
        # Create database session
        # ========================================================================
        yield session
    finally:
        session.close()
