"""
Author: Lav Sharma
Created on: 5th Dec 2023
"""

from sqlalchemy import Column, BIGINT, SMALLINT, VARCHAR, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Coupon(Base):
    __tablename__ = 'Coupon'
    C_Id = Column(BIGINT, primary_key=True)
    C_Name = Column(VARCHAR(255), nullable=False, unique=True)
    C_GlobalTotalRepeatCount = Column(BIGINT, nullable=False)
    C_UserTotalRepeatCount = Column(BIGINT, nullable=False)
    C_UserDailyRepeatCount = Column(BIGINT, nullable=False)
    C_UserWeeklyRepeatCount = Column(BIGINT, nullable=False)


class User(Base):
    __tablename__ = 'User'
    U_Id = Column(BIGINT, primary_key=True)
    U_Name = Column(VARCHAR(255), nullable=False, unique=True)


class CouponUsageLog(Base):
    __tablename__ = 'CouponUsageLog'
    CUL_ID = Column(BIGINT, primary_key=True)
    C_Id = Column(BIGINT, nullable=False)
    U_Id = Column(SMALLINT, nullable=False)
    CUL_Timestamp = Column(DATETIME, nullable=False)
