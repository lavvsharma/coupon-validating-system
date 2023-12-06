from typing import Optional

from pydantic import BaseModel


class HeartbeatResult(BaseModel):
    is_alive: bool


class Coupon(BaseModel):
    Coupon_Name: str
    Global_Total_Repeat_Count: int = 10000
    User_Total_Repeat_Count: int = 3
    User_Daily_Repeat_Count: int = 1
    User_Weekly_Repeat_Count: int = 1

    def __repr__(self):
        return {
            "Coupon_Name": self.Coupon_Name,
            "Global_Total_Repeat_Count": self.Global_Total_Repeat_Count,
            "User_Total_Repeat_Count": self.User_Total_Repeat_Count,
            "User_Daily_Repeat_Count": self.User_Daily_Repeat_Count,
            "User_Weekly_Repeat_Count": self.User_Weekly_Repeat_Count
        }


class UpdateCoupon(BaseModel):
    Coupon_Name: str
    Global_Total_Repeat_Count: Optional[int]
    User_Total_Repeat_Count: Optional[int]
    User_Daily_Repeat_Count: Optional[int]
    User_Weekly_Repeat_Count: Optional[int]

    def __repr__(self):
        return {
            "Coupon_Name": self.Coupon_Name,
            "Global_Total_Repeat_Count": self.Global_Total_Repeat_Count,
            "User_Total_Repeat_Count": self.User_Total_Repeat_Count,
            "User_Daily_Repeat_Count": self.User_Daily_Repeat_Count,
            "User_Weekly_Repeat_Count": self.User_Weekly_Repeat_Count
        }


class ApplyCoupon(BaseModel):
    Coupon_Name: str
    Username: str

    def __repr__(self):
        return {
            "Coupon_Name": self.Coupon_Name,
            "Username": self.Username
        }
