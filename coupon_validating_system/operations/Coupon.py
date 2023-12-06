"""
Author: Lav Sharma
Created on: 5th Dec 2023
"""

from retrying import retry
from sqlalchemy import exists
from sqlalchemy.exc import ProgrammingError, DatabaseError, OperationalError

import coupon_validating_system.configuration as config
from coupon_validating_system.CommonEnums import ResponseCode, HttpResponseCode
from coupon_validating_system.ModuleLogger import setup_logger
from coupon_validating_system.database.Session import get_db
from coupon_validating_system.entity.DatabaseModels import Coupon
from coupon_validating_system.exception import SQLException

logger = setup_logger()


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def create_entry_in_coupon(coupon: dict) -> dict:
    """
        Description: This function is used to create a coupon in the Coupon table. It will first check if the
        coupon name is already present in the database or not.
        If Yes --> It will not create an entry.
        If No --> It will create an entry in the Coupon table.
    """
    create_response = dict()
    try:
        # ========================================================================
        # Check if the coupon name is already present in the Coupon table
        # ========================================================================
        check_coupon_name_exists = check_if_coupon_name_exists_in_coupon(coupon['Coupon_Name'])
        if check_coupon_name_exists:
            # ========================================================================
            # Coupon already exists in the Coupon table with the same name
            # ========================================================================
            create_response['Entry_Created'] = False
            create_response['ResponseCode'] = ResponseCode.Record_Already_Exists.value

        else:
            # ========================================================================
            # Coupon does not exist in Coupon table with coupon name, create Coupon
            # ========================================================================
            coupon_entry = Coupon(C_Name=coupon['Coupon_Name'],
                                  C_GlobalTotalRepeatCount=coupon['Global_Total_Repeat_Count'],
                                  C_UserTotalRepeatCount=coupon['User_Total_Repeat_Count'],
                                  C_UserDailyRepeatCount=coupon['User_Daily_Repeat_Count'],
                                  C_UserWeeklyRepeatCount=coupon['User_Weekly_Repeat_Count'])

            with get_db() as session_object:
                try:
                    # ========================================================================
                    # Create entry in the Coupon table
                    # ========================================================================
                    session_object.add(coupon_entry)
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
                    logger.error('Error in creating entry in Coupon' +
                                 f'\nError - {str(error)}', exc_info=True)

                    create_response['Entry_Created'] = False
                    create_response['ResponseCode'] = ResponseCode.Record_Create_Fail.value

                # ========================================================================
                # Retrieve the added row
                # ========================================================================
                added_row = session_object.query(coupon_entry.__class__).get(coupon_entry.C_Id)

            if added_row:
                # ========================================================================
                # Entry successfully created in the db
                # ========================================================================
                logger.info('Entry created in Coupon table')
                create_response['Entry_Created'] = True
                create_response['ResponseCode'] = ResponseCode.Record_Create_Success.value

            else:
                logger.error('Error in creating entry in Coupon', exc_info=True)
                create_response['Entry_Created'] = False
                create_response['ResponseCode'] = ResponseCode.Record_Create_Fail.value

        create_response['HttpResponseCode'] = HttpResponseCode.Success.value
        create_response['Input'] = dict()
        create_response['Input']['Coupon_Name'] = coupon['Coupon_Name']
        create_response['Input']['Global_Total_Repeat_Count'] = coupon['Global_Total_Repeat_Count']
        create_response['Input']['User_Total_Repeat_Count'] = coupon['User_Total_Repeat_Count']
        create_response['Input']['User_Daily_Repeat_Count'] = coupon['User_Daily_Repeat_Count']
        create_response['Input']['User_Weekly_Repeat_Count'] = coupon['User_Weekly_Repeat_Count']
        return create_response

    except Exception as error:
        logger.error(f'Error in creating entry in Coupon, Exception - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def check_if_coupon_name_exists_in_coupon(coupon_name: str) -> bool:
    """
        Description: This function is used to check that given a coupon_name whether a record exists in the Coupon
        table or not.
        If Yes --> Returns True
        Else --> Returns False
    """
    record_exists = False
    try:
        with get_db() as session_object:
            if session_object.query(exists().where(Coupon.C_Name == coupon_name)).scalar():
                record_exists = True

            return record_exists

    except ProgrammingError as mysql_programming_error:
        logger.error('Wrong/Invalid/Unknown database name provided' +
                     f'\nError-{str(mysql_programming_error)}', exc_info=True)
        raise mysql_programming_error

    except DatabaseError as mysql_database_error:
        logger.error('Error connecting to the MYSQL Server.Invalid database IP or Port provided' +
                     f'\nError-{str(mysql_database_error)}', exc_info=True)
        raise mysql_database_error

    except Exception as error:
        logger.error(f'Error in exists query of the database, Coupon Name - {str(coupon_name)}' +
                     f'\nException - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def read_row_from_coupon(coupon_name: str):
    """
        Description: This function is used to read a row from the Coupon table, given a coupon_name.
    """
    try:
        read_row_output = dict()

        with get_db() as session_object:
            row_entry = session_object.query(Coupon).filter(Coupon.C_Name == coupon_name).first()
            read_row_output['Row'] = vars(row_entry)
            read_row_output['ResponseCode'] = ResponseCode.Record_Read_Success.value

        read_row_output['Input'] = dict()
        read_row_output['Input']['Coupon_Name'] = coupon_name
        read_row_output['HttpResponseCode'] = HttpResponseCode.Success.value
        return read_row_output

    except ProgrammingError as mysql_programming_error:
        logger.error('Wrong/Invalid/Unknown database name provided' +
                     f'\nError-{str(mysql_programming_error)}', exc_info=True)
        raise mysql_programming_error

    except DatabaseError as mysql_database_error:
        logger.error('Error connecting to the MYSQL Server.Invalid database IP or Port provided' +
                     f'\nError-{str(mysql_database_error)}', exc_info=True)
        raise mysql_database_error

    except Exception as error:
        logger.error(f'Error in retrieving row from Coupon, for Coupon Name - {str(coupon_name)}'
                     + f'\nException - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def read_all_coupons():
    """
        Description - This function is used to read all the coupons from the Coupon table.
    """
    try:
        output_response = dict()

        with get_db() as session_object:
            # ========================================================================
            # Fetch all the rows from Coupon table
            # ========================================================================
            row_entry = session_object.query(Coupon).all()
            user_rows = [{"Coupon_Name": row.C_Name} for row in row_entry]

        output_response['Coupons'] = user_rows
        output_response['HttpResponseCode'] = HttpResponseCode.Success.value
        return output_response

    except ProgrammingError as mysql_programming_error:
        logger.error('Wrong/Invalid/Unknown database name provided' +
                     f'\nError-{str(mysql_programming_error)}', exc_info=True)
        raise mysql_programming_error

    except DatabaseError as mysql_database_error:
        logger.error('Error connecting to the MYSQL Server.Invalid database IP or Port provided' +
                     f'\nError-{str(mysql_database_error)}', exc_info=True)
        raise mysql_database_error

    except Exception as error:
        logger.error(f'Error in retrieving all rows from Coupon table'
                     + f'\nException - {str(error)}', exc_info=True)
