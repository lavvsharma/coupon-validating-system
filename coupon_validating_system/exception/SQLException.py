"""
Author: Lav Sharma
Created on: 5th Dec 2023
"""

from sqlalchemy.exc import ProgrammingError, DatabaseError, OperationalError


def retry_if_mysql_error(exception: Exception) -> bool:
    """Return True if we should retry (in this case when it's an DatabaseError), False otherwise"""

    is_database_error = isinstance(exception, DatabaseError)
    is_programming_error = isinstance(exception, ProgrammingError)
    is_operational_error = isinstance(exception, OperationalError)

    if is_database_error:
        return True

    elif is_programming_error:
        return True

    elif is_operational_error:
        return True
