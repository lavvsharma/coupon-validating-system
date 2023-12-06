"""
Author: Lav Sharma
Created on: 5th Dec 2023
"""

import configparser
import os

# ===================================================================
# Get the package relative's path
# ===================================================================
lstr_package_path = os.path.dirname(os.path.realpath(__file__))

# ===================================================================
# Generate the config file path
# ===================================================================
lstr_config_file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + \
                        os.path.sep + "config.ini"

# ===================================================================
# Create the configparser object
# ===================================================================
lobj_config = configparser.ConfigParser()

# ===================================================================
# Read the config.ini file
# ===================================================================
lobj_config.read(lstr_config_file_path)

# ===================================================================
# Get the sections present in the config.ini
# ===================================================================
config_sections = lobj_config.sections()

# ===================================================================
# Check if the GENERAL section is present in the config.ini
# ===================================================================
if 'GENERAL' in config_sections:
    # ===================================================================
    # If present, then read all the GENERAL section variables
    # ===================================================================
    MODULE_NAME = str(lobj_config['GENERAL']['MODULE_NAME'])

    ALLOWED_METHODS = eval(lobj_config['GENERAL']['ALLOWED_METHODS'])
    ALLOW_HEADERS = eval(lobj_config['GENERAL']['ALLOW_HEADERS'])

# ===================================================================
# Check if the ENVIRONMENT section is present in the config.ini
# ===================================================================
if 'ENVIRONMENT' in config_sections:
    # ===================================================================
    # If present, then read all the ENVIRONMENT section variables
    # ===================================================================
    HOST_PROTOCOL = str(lobj_config['ENVIRONMENT']['HOST_PROTOCOL'])
    HOST_IP = str(lobj_config['ENVIRONMENT']['HOST_IP'])
    HOST_PORT = int(lobj_config['ENVIRONMENT']['HOST_PORT'])

    ORIGINS = eval(lobj_config['ENVIRONMENT']['ORIGINS'])
    ALLOW_CREDENTIALS = str(lobj_config['ENVIRONMENT']['ALLOW_CREDENTIALS'])
    IS_DEBUG = str(lobj_config['ENVIRONMENT']['IS_DEBUG'])

    DATABASE_HOST = str(lobj_config['ENVIRONMENT']['DATABASE_HOST'])
    DATABASE_PORT = str(lobj_config['ENVIRONMENT']['DATABASE_PORT'])

    DATABASE_NAME = str(lobj_config['ENVIRONMENT']['DATABASE_NAME'])
    DATABASE_USERNAME = str(lobj_config['ENVIRONMENT']['DATABASE_USERNAME'])
    DATABASE_PASSWORD = str(lobj_config['ENVIRONMENT']['DATABASE_PASSWORD'])

    RETRY_ATTEMPT_FOR_DATABASE_CONNECTION = int(lobj_config['ENVIRONMENT']['RETRY_ATTEMPT_FOR_DATABASE_CONNECTION'])
    WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS = int(lobj_config['ENVIRONMENT'][
                                                         'WAITING_TIME_BETWEEN_RETRY_IN_MILLISECONDS'])
    MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS = int(lobj_config['ENVIRONMENT'][
                                                             'MAXIMUM_WAITING_TIME_FOR_RETRY_IN_MILLISECONDS'])

    LOGGING_LEVEL = str(lobj_config['ENVIRONMENT']['LOGGING_LEVEL'])
