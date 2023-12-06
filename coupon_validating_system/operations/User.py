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
from coupon_validating_system.entity.DatabaseModels import User
from coupon_validating_system.exception import SQLException

logger = setup_logger()


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def create_entry_in_user(username: str) -> dict:
    """
        Description: This function is used to create a User in the User table given a username.
        It will first check if the username is already present in the User table or not.
        If user exists --> Do not create a User in the User table.
        If user does not exist --> Create User in the User table.
    """
    create_response = dict()
    try:
        # ========================================================================
        # Check if the username is already present in the User table
        # ========================================================================
        check_user_exists = check_if_username_exists_in_user(username)
        if check_user_exists:
            # ========================================================================
            # User already exists in the User table with the same name
            # ========================================================================
            create_response['Entry_Created'] = False
            create_response['ResponseCode'] = ResponseCode.Record_Already_Exists.value

        else:
            # ========================================================================
            # User does not exist in User table with username, create User
            # ========================================================================
            user_entry = User(U_Name=username)
            with get_db() as session_object:
                try:
                    # ========================================================================
                    # Create entry in the User table
                    # ========================================================================
                    session_object.add(user_entry)
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
                    logger.error('Error in creating entry in User' +
                                 f'\nError - {str(error)}', exc_info=True)

                    create_response['Entry_Created'] = False
                    create_response['ResponseCode'] = ResponseCode.Record_Create_Fail.value

                # ========================================================================
                # Retrieve the added row
                # ========================================================================
                added_row = session_object.query(user_entry.__class__).get(user_entry.U_Id)

            if added_row:
                # ========================================================================
                # Entry successfully created in the db
                # ========================================================================
                logger.info('Entry created in User')
                create_response['Entry_Created'] = True
                create_response['User_Id'] = vars(added_row)['U_Id']
                create_response['ResponseCode'] = ResponseCode.Record_Create_Success.value

            else:
                logger.error('Error in creating entry in User', exc_info=True)
                create_response['Entry_Created'] = False
                create_response['ResponseCode'] = ResponseCode.Record_Create_Fail.value

        create_response['HttpResponseCode'] = HttpResponseCode.Success.value
        create_response['Input'] = dict()
        create_response['Input']['Username'] = username
        return create_response

    except Exception as error:
        logger.error(f'Error in creating entry in User table'
                     f'Input: Username - {str(username)}, Exception - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def check_if_username_exists_in_user(username: str) -> bool:
    """
        Description: This function is used to check that given a username whether a record exists in the User
        table or not.
        If Yes --> Returns True
        Else --> Returns False
    """
    record_exists = False
    try:
        with get_db() as session_object:
            if session_object.query(exists().where(User.U_Name == username)).scalar():
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
        logger.error(f'Error in exists query of the database, Username - {str(username)}' +
                     f'\nException - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def read_row_from_user(username: str):
    """
        Description: This function is used to read a row from the User table given a username.
    """
    try:
        read_row_output = dict()

        with get_db() as session_object:
            row_entry = session_object.query(User).filter(User.U_Name == username).first()
            read_row_output['Row'] = vars(row_entry)
            read_row_output['ResponseCode'] = ResponseCode.Record_Read_Success.value

        read_row_output['Input'] = dict()
        read_row_output['Input']['Coupon_Name'] = username
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
        logger.error(f'Error in retrieving row from User, for Username - {str(username)}'
                     + f'\nException - {str(error)}', exc_info=True)


@retry(stop_max_attempt_number=config.RETRY_ATTEMPT_FOR_DATABASE_CONNECTION,
       wait_exponential_multiplier=config.WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS,
       wait_exponential_max=config.MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS,
       retry_on_exception=SQLException.retry_if_mysql_error)
def read_all_users():
    """
        Description: This function is used to read all the rows from the User table.
    """
    try:
        output_response = dict()

        with get_db() as session_object:
            # ========================================================================
            # Fetch all the rows from User table
            # ========================================================================
            row_entry = session_object.query(User).all()
            user_rows = [{"Username": row.U_Name} for row in row_entry]

        output_response['Users'] = user_rows
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
        logger.error(f'Error in retrieving all rows from User table'
                     + f'\nException - {str(error)}', exc_info=True)
