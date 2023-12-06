"""
Author: Lav Sharma
Created on: 5th Dec 2023
"""

from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import coupon_validating_system.configuration as config
from coupon_validating_system import __appname__, __version__, __description__
from coupon_validating_system.ModuleLogger import setup_logger
from coupon_validating_system.entity.Models import Coupon, ApplyCoupon
from coupon_validating_system.entity.Models import HeartbeatResult
from coupon_validating_system.operations.Coupon import create_entry_in_coupon, check_if_coupon_name_exists_in_coupon, \
    read_row_from_coupon, read_all_coupons
from coupon_validating_system.operations.CouponUsageLog import count_all_rows_given_coupon_id, \
    count_all_rows_given_coupon_id_and_user_id, count_all_rows_given_coupon_id_and_user_id_for_a_day, \
    count_all_rows_given_coupon_id_and_user_id_for_a_week, create_entry_in_coupon_usage_log
from coupon_validating_system.operations.User import create_entry_in_user, check_if_username_exists_in_user, \
    read_row_from_user, read_all_users

logger = setup_logger()


class CouponValidatingSystem:
    def __init__(self, appname, version, description):
        try:
            self.app = FastAPI(title=appname, version=version, description=description)
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=config.ORIGINS,
                allow_credentials=config.ALLOW_CREDENTIALS,
                allow_methods=config.ALLOWED_METHODS,
                allow_headers=config.ALLOW_HEADERS,
            )
            self.add_routes()

        except Exception as error:
            logger.error(f'Exception - {str(error)}', exc_info=True)

    def add_routes(self):
        @self.app.get('/healthcheck', tags=['Heartbeat'])
        async def get_heartbeat():
            """
            This API call is used to check Healthcheck of Coupon Validating System.
            """
            try:
                heartbeat = HeartbeatResult(is_alive=True)

                return {
                    'IsAlive': heartbeat.is_alive,
                    'AppName': __appname__,
                    'Version': __version__,
                    'Description': __description__
                }

            except Exception as error:
                logger.error(f'Exception - {str(error)}', exc_info=True)

        @self.app.post('/create/user', tags=['User'])
        async def create_user(username: str):
            """
            This API is used to create a user in the User table. With the help of username a user can redeem the coupon.
            """
            try:
                return create_entry_in_user(username)

            except Exception as error:
                logger.error(f'Exception - {str(error)}'
                             f'Input: Username - {str(username)}', exc_info=True)

        @self.app.get('/read/all/user/', tags=['User'])
        async def read_all_user():
            """
            This API is used to read all the users from the User table. It will return all the username that are present
            in the User table.
            """
            try:
                return read_all_users()

            except Exception as error:
                logger.error(f'Exception - {str(error)}', exc_info=True)

        @self.app.post('/create/coupon', tags=['Coupon'])
        async def create_coupon(coupon: Coupon):
            """
            This API is used to create a coupon in the system. With the help of the added configuration we will be
            able to add a limiter to our coupon so that a single coupon is not used ‘n’ or many times.
            """
            try:
                _coupon = coupon.__repr__()
                return create_entry_in_coupon(_coupon)

            except Exception as error:
                logger.error(f'Exception - {str(error)}'
                             f'Input: {str(coupon)}', exc_info=True)

        @self.app.get('/read/all/coupon/', tags=['Coupon'])
        async def read_all_coupon():
            """
            This API is used to read all the coupons from the Coupon table. It will return all the coupons
            that are present in the Coupon table.
            """
            try:
                return read_all_coupons()

            except Exception as error:
                logger.error(f'Exception - {str(error)}', exc_info=True)

        @self.app.post('/apply/coupon', tags=['Coupon'])
        async def apply_coupon(apply_coupon: ApplyCoupon):
            """
            This API is used to apply the coupon for a particular user. This API will first validate the existence of
            the coupon and the adherence to repeat count configurations for the respective coupon.
            """
            output_response = dict()
            try:
                _apply_coupon = apply_coupon.__repr__()
                current_utc_timestamp = datetime.utcnow()

                # ========================================================================
                # Check if the user is valid
                # ========================================================================
                username = _apply_coupon['Username']
                is_valid_user = check_if_username_exists_in_user(username)
                if is_valid_user:
                    # ========================================================================
                    # Check if the coupon is valid
                    # ========================================================================
                    coupon_name = _apply_coupon['Coupon_Name']
                    is_coupon_valid = check_if_coupon_name_exists_in_coupon(coupon_name)
                    if is_coupon_valid:
                        # ========================================================================
                        # Read the coupon
                        # ========================================================================
                        coupon_row = read_row_from_coupon(coupon_name)
                        coupon_id = coupon_row['Row']['C_Id']
                        global_repeat_count = coupon_row['Row']['C_GlobalTotalRepeatCount']
                        user_repeat_count = coupon_row['Row']['C_UserTotalRepeatCount']
                        user_weekly_repeat_count = coupon_row['Row']['C_UserWeeklyRepeatCount']
                        user_daily_repeat_count = coupon_row['Row']['C_UserDailyRepeatCount']

                        # ========================================================================
                        # Get the total number of count i.e. How many times till date the coupon is used
                        # ========================================================================
                        coupon_global_count = count_all_rows_given_coupon_id(coupon_id)
                        if coupon_global_count >= global_repeat_count:
                            message = 'Coupon has been exhausted'

                        else:
                            # ========================================================================
                            # Read user row
                            # ========================================================================
                            user_row = read_row_from_user(username)
                            user_id = user_row['Row']['U_Id']

                            # ========================================================================
                            # Get the count of how many times has the user used this particular coupon in total
                            # ========================================================================
                            coupon_and_user_count = count_all_rows_given_coupon_id_and_user_id(coupon_id, user_id)

                            if coupon_and_user_count >= user_repeat_count:
                                message = 'User has exhausted the number of times he/she can use a particular coupon'

                            else:
                                # ========================================================================
                                # Check the weekly repeat count
                                # ========================================================================
                                coupon_and_user_weekly_count = count_all_rows_given_coupon_id_and_user_id_for_a_week(
                                    coupon_id, user_id, current_utc_timestamp
                                )

                                if coupon_and_user_weekly_count >= user_weekly_repeat_count:
                                    message = 'User has exhausted the number of times he/she can use a particular coupon in a week'

                                else:
                                    coupon_and_user_daily_count = count_all_rows_given_coupon_id_and_user_id_for_a_day(
                                        coupon_id, user_id, current_utc_timestamp)

                                    if coupon_and_user_daily_count >= user_daily_repeat_count:
                                        message = 'User has exhausted the number of times he/she can use a particular coupon in a day'

                                    else:
                                        # ========================================================================
                                        # Allow the usage of coupon, make entry in the CouponUsageLog
                                        # ========================================================================
                                        create_entry_in_coupon_usage_log(coupon_id, user_id, current_utc_timestamp)
                                        message = 'Redeemed discount'

                    else:
                        message = 'Not a valid coupon'

                else:
                    message = 'Not a valid user'

                output_response['Username'] = _apply_coupon['Username']
                output_response['Coupon_Name'] = _apply_coupon['Coupon_Name']
                output_response['Message'] = message
                return output_response

            except Exception as error:
                logger.error(f'Exception - {str(error)}'
                             f'Input: {str(apply_coupon)}', exc_info=True)

    def run(self, host, port):
        try:
            logger.info(f'Started Coupon Validating System on {str(host)}:{str(port)}')
            uvicorn.run(self.app, host=host, port=port)

        except Exception as error:
            logger.error(f'Exception - {str(error)}', exc_info=True)


if __name__ == "__main__":
    app = CouponValidatingSystem(appname=__appname__, version=__version__, description=__description__)
    app.run(host=config.HOST_IP, port=config.HOST_PORT)
