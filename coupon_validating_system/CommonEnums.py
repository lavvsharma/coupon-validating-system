"""
Author: Lav Sharma
Created on: 5th Dec 2023
"""

from enum import Enum


class ResponseCode(Enum):
    Record_Create_Success = 2000
    Record_Read_Success = 2001
    Record_Update_Success = 2002
    Record_Found = 2003
    Record_Create_Fail = 3000
    Record_Read_Fail = 3001
    Record_Update_Fail = 3002
    Record_Not_Found = 3003
    Record_Already_Exists = 3004
    Column_Does_Not_Exists = 3005
    Invalid_Order_By_Choice = 3006
    Database_Error = 4000


class HttpResponseCode(Enum):
    Success = 200
    Error = 404
