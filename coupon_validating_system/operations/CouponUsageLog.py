"""
Author: Lav Sharma
Created on: 6th Dec 2023
"""

from datetime import datetime, timedelta

from retrying import retry
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.exc import ProgrammingError, DatabaseError, OperationalError

import coupon_validating_system.configuration as config
from coupon_validating_system.CommonEnums import ResponseCode, HttpResponseCode
from coupon_validating_system.ModuleLogger import setup_logger
from coupon_validating_system.database.Session import get_db
from coupon_validating_system.entity.DatabaseModels import CouponUsageLog
from coupon_validating_system.exception import SQLException

logger = setup_logger()


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def create_entry_in_coupon_usage_log(coupon_id: int,
                                     user_id: int,
                                     query_timestamp: datetime) -> dict:
    """
        Description: This function is used to create an entry in the CouponUsageLog table.
    """
    create_response = dict()
    try:
        coupon_usage_log_entry = CouponUsageLog(C_Id=coupon_id,
                                                U_Id=user_id,
                                                CUL_Timestamp=query_timestamp)

        with get_db() as session_object:
            try:
                # ========================================================================
                # Create entry in the CouponUsageLog table
                # ========================================================================
                session_object.add(coupon_usage_log_entry)
                session_object.commit()

            except OperationalError as operational_error:
                logger.error('Error connecting to the MYSQL Server.Invalid database IP or Port provided' +
                             f'\nError-{str(operational_error)}', exc_info=True)
                raise operational_error

            except ProgrammingError as programming_error:
                logger.error('Wrong/Invalid/Unknown database name provided' +
                             f'\nError-{str(programming_error)}', exc_info=True)
                raise programming_error

            except Exception as error:
                # ========================================================================
                # Handle the exception and rollback the session_object
                # ========================================================================
                session_object.rollback()
                logger.error('Error in creating entry in CouponUsageLog table' +
                             f'\nError - {str(error)}', exc_info=True)
                create_response['Entry_Created'] = False
                create_response['ResponseCode'] = ResponseCode.Record_Create_Fail.value

            # ========================================================================
            # Retrieve the added row
            # ========================================================================
            added_row = session_object.query(coupon_usage_log_entry.__class__).get(coupon_usage_log_entry.CUL_ID)

            if added_row:
                # ========================================================================
                # Entry successfully created in the db
                # ========================================================================
                logger.info('Entry created in CouponUsageLog')
                create_response['Entry_Created'] = True
                create_response['ResponseCode'] = ResponseCode.Record_Create_Success.value

            else:
                logger.error('Error in creating entry in CouponUsageLog table', exc_info=True)
                create_response['Entry_Created'] = False
                create_response['ResponseCode'] = ResponseCode.Record_Create_Fail.value

        create_response['HttpResponseCode'] = HttpResponseCode.Success.value
        create_response['Input'] = dict()
        create_response['Input']['Coupon_Id'] = coupon_id
        create_response['Input']['User_Id'] = user_id
        create_response['Input']['Query_Timestamp'] = query_timestamp
        return create_response

    except Exception as error:
        logger.error(f'Error in creating entry in CouponUsageLog, Exception - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def count_all_rows_given_coupon_id(coupon_id: int) -> int:
    """
        Description - This function is used to count all the rows from the Coupon table given a coupon_id.
    """
    try:
        with get_db() as session_object:
            row_count = session_object.query(func.count(CouponUsageLog.C_Id)).filter(
                CouponUsageLog.C_Id == coupon_id).scalar()
        return row_count

    except ProgrammingError as mysql_programming_error:
        logger.error('Wrong/Invalid/Unknown database name provided' +
                     f'\nError-{str(mysql_programming_error)}', exc_info=True)
        raise mysql_programming_error

    except DatabaseError as mysql_database_error:
        logger.error('Error connecting to the MYSQL Server.Invalid database IP or Port provided' +
                     f'\nError-{str(mysql_database_error)}', exc_info=True)
        raise mysql_database_error

    except Exception as error:
        logger.error(f'Error in retrieving all rows from CouponUsageLog, for CouponId - {str(coupon_id)}'
                     + f'\nException - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def count_all_rows_given_coupon_id_and_user_id(coupon_id: int,
                                               user_id: int) -> int:
    """
        Description - This function is used to count all the rows from the CouponUsageLog table given a
        coupon_id and user_id.
    """
    try:
        with get_db() as session_object:
            row_count = session_object.query(func.count(CouponUsageLog.C_Id)).filter(
                and_(CouponUsageLog.C_Id == coupon_id, CouponUsageLog.U_Id == user_id)
            ).scalar()

        return row_count

    except ProgrammingError as mysql_programming_error:
        logger.error('Wrong/Invalid/Unknown database name provided' +
                     f'\nError-{str(mysql_programming_error)}', exc_info=True)
        raise mysql_programming_error

    except DatabaseError as mysql_database_error:
        logger.error('Error connecting to the MYSQL Server.Invalid database IP or Port provided' +
                     f'\nError-{str(mysql_database_error)}', exc_info=True)
        raise mysql_database_error

    except Exception as error:
        logger.error(f'Error in retrieving all rows from CouponUsageLog, for CouponId - {str(coupon_id)},'
                     f'UserId - {str(user_id)}'
                     + f'\nException - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def count_all_rows_given_coupon_id_and_user_id_for_a_day(coupon_id: int,
                                                         user_id: int,
                                                         query_timestamp: datetime) -> int:
    """
        Description - This function is used to count all the rows from the CouponUsageLog table given a
        coupon_id and user_id for a single day.
    """
    try:
        with get_db() as session_object:
            # ========================================================================
            # Calculate the start and end times based on the given timestamp for a day
            # ========================================================================
            start_timestamp = query_timestamp.replace(hour=0, minute=0, second=0)
            end_timestamp = start_timestamp + timedelta(days=1) - timedelta(seconds=1)

            row_count = session_object.query(func.count(CouponUsageLog.C_Id)).filter(
                and_(
                    CouponUsageLog.C_Id == coupon_id,
                    CouponUsageLog.U_Id == user_id,
                    CouponUsageLog.CUL_Timestamp.between(start_timestamp, end_timestamp)
                )
            ).scalar()

        return row_count

    except ProgrammingError as mysql_programming_error:
        logger.error('Wrong/Invalid/Unknown database name provided' +
                     f'\nError-{str(mysql_programming_error)}', exc_info=True)
        raise mysql_programming_error

    except DatabaseError as mysql_database_error:
        logger.error('Error connecting to the MYSQL Server.Invalid database IP or Port provided' +
                     f'\nError-{str(mysql_database_error)}', exc_info=True)
        raise mysql_database_error

    except Exception as error:
        logger.error(f'Error in retrieving all rows from CouponUsageLog, for CouponId - {str(coupon_id)}'
                     f', UserId - {str(user_id)}'
                     f', Query Timestamp - {str(query_timestamp)}'
                     + f'\nException - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def count_all_rows_given_coupon_id_and_user_id_for_a_week(coupon_id: int,
                                                          user_id: int,
                                                          query_timestamp: datetime) -> int:
    """
        Description - This function is used to count all the rows from the CouponUsageLog table given a
        coupon_id and user_id for a week.
    """
    try:
        with get_db() as session_object:
            # ========================================================================
            # Calculate the start and end times based on the current UTC timestamp for a week
            # ========================================================================
            start_timestamp = query_timestamp - timedelta(days=7)
            start_timestamp = start_timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

            end_timestamp = query_timestamp.replace(hour=23, minute=59, second=59, microsecond=999999)

            row_count = session_object.query(func.count(CouponUsageLog.C_Id)).filter(
                and_(
                    CouponUsageLog.C_Id == coupon_id,
                    CouponUsageLog.U_Id == user_id,
                    CouponUsageLog.CUL_Timestamp.between(start_timestamp, end_timestamp)
                )
            ).scalar()

        return row_count

    except ProgrammingError as mysql_programming_error:
        logger.error('Wrong/Invalid/Unknown database name provided' +
                     f'\nError-{str(mysql_programming_error)}', exc_info=True)
        raise mysql_programming_error

    except DatabaseError as mysql_database_error:
        logger.error('Error connecting to the MYSQL Server.Invalid database IP or Port provided' +
                     f'\nError-{str(mysql_database_error)}', exc_info=True)
        raise mysql_database_error

    except Exception as error:
        logger.error(f'Error in retrieving all rows from CouponUsageLog, for CouponId - {str(coupon_id)}'
                     f', UserId - {str(user_id)}'
                     f', Query Timestamp - {str(query_timestamp)}'
                     + f'\nException - {str(error)}', exc_info=True)
