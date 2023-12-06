# coupon_validating_system

### Installation

To run this it can be directly installed by using python pip / pip3

```sh
$ pip3 install coupon_validating_system==1.0.0
```

### File Structure

```
├── coupon_validating_system
|   └── data
|       └── config.ini
|   └── database
|       └── __init__.py
|       └── Connection.py
|       └── Session.py
|   └── entity
|       └── __init__.py
|       └── DatabaseModels.py
|       └── Models.py
|   └── exception
|       └── __init__.py
|       └── SQLException.py
|   └── operations
|       └── __init__.py
|       └── Coupon.py
|       └── CouponUsageLog.py
|       └── User.py
|   ├── __init__.py
|   ├── CommonEnums.py
|   ├── configuration.py
|   ├── CouponValidatingSystem.py
|   ├── ModuleLogger.py
├── MANIFEST.in                  
├── README.md
└── setup.py
```

## Documents

1. Import the [database](https://drive.google.com/file/d/1lzRI8e5Joh27lU-94SKmxGgKy2WkyRMb/view?usp=sharing) before going ahead with the execution.
2. Database design document can be found [here](https://docs.google.com/spreadsheets/d/1RdbKFKGky1J4wFwCQzYAo4hMC_x2Ch5rOO5VNMuqGSk/edit?usp=sharing).
3. Design document related to APIs and function can be found [here](https://docs.google.com/document/d/1jY4K5CNO3G7Ab2GR0yUced5utoT1uqgPOXs1neTAR9M/edit?usp=sharing).
4. Postman collection can be found [here](https://drive.google.com/file/d/1ZK1qZ39Pv2oLDz3QReN3bGNsPYCKjU75/view?usp=sharing).
5. Video explanation of the project can be found [here](https://www.loom.com/share/55a8f2ab5fc8474abc07aeac2f34e7da?sid=3393d76e-c9e1-4d21-a429-f1add31650e3).

## Requirements
1. Python3.9
2. MySQL
3. MySQL workbench 

## Installation
1. Create a python-virtual environment using the below command for python3.9

```bash
python3.9 -m venv venv
```

2. Navigate to the setup.py.
3. Enter the below command to install all the required packages

```bash
pip install .
```

## APIs
Below are the APIs implemented in the coupon_validating_system FastAPI service. 
1. /create/user
    1. This API is used to create a user in the system. With the help of user id or username a user can make use of the coupon.
    2. cURL command
   
   ```bash
    curl -X 'POST' \
      'http://localhost:5000/create/user?username=lavsharma' \
      -H 'accept: application/json' \
      -d ''
   ```
   
2. /read/all/user
    1. This API is used to read all the users that are present in the User table.
    2. cURL command
    
   ```bash
    curl -X 'GET' \
      'http://localhost:5000/read/all/user/' \
      -H 'accept: application/json'
   ```

3. /create/coupon
    1. This API is used to create a coupon in the system. With the help of the added configuration we will be able to add a limiter to our coupon so that a single coupon is not used ‘n’ or many times.
    2. cURL command
    
   ```bash
    curl -X 'POST' \
      'http://localhost:5000/create/coupon' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "Coupon_Name": "holiday coupon",
      "Global_Total_Repeat_Count": 10000,
      "User_Total_Repeat_Count": 3,
      "User_Daily_Repeat_Count": 1,
      "User_Weekly_Repeat_Count": 1
    }'
   ```

4. /read/all/coupon
    1. This API is used to read all the coupons from the Coupon table.
    2. cURL command
    
   ```bash
    curl -X 'GET' \
      'http://localhost:5000/read/all/coupon/' \
      -H 'accept: application/json'
    ```
   
5. /apply/coupon
    1. This API is used to apply the coupon for a particular user.
    2. This API will first validate the existence of the coupon and the adherence to repeat count configurations for the respective coupon.
    3. cURL command
    
   ```bash
    curl -X 'POST' \
      'http://localhost:5000/apply/coupon' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "Coupon_Name": "holiday coupon",
      "Username": "lavsharma"
    }'
   ```

