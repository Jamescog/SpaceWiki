from pydantic import BaseModel, EmailStr, Field


class UserSignupDefault(BaseModel):
    """
    Represents the schema for user signup.

    Attributes:
        username (str): The username of the user (required).
        password (str): The password of the user.
        email (str): The email of the user.

    """
    username: str
    password: str = Field(..., min_length=4)
    email: EmailStr = None

    class Config:
        """example schema for the username, password and email"""
        json_schema_extra = {
            "examples": [
                {
                    "username": "SpaceInvader",
                    "email": "mars32@gmail.com",
                    "password": "password123"
                }
            ]
        }


class UserLoginDefault(BaseModel):
    """
    Represents the schema for user login.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.

    """
    username: str
    password: str

    class Config:
        """example schema for the username and password"""
        json_schema_extra = {
            "example": {
                "username": "SpaceInvader",
                "password": "password123"
            }
        }


class SignupSuccess(BaseModel):
    """Represents the schema for user signup success.

    Attributes:
        message (str): The message to be displayed to the user.
    """

    message: str

    class Config:
        """example schema for the message"""
        json_schema_extra = {
            "example": {
                "message": "User created successfully."
            }
        }


class LoginSuccess(BaseModel):
    """
    Represents the schema for user login success.

    Attributes:
        token (str): The token of the user.

    """
    token: str

    class Config:
        """example schema for the token"""
        json_schema_extra = {
            "example": {
                "token": """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiJzcGFjZWludmFkZXIiLCJleHAiOjE2MTM0NzY1NjB9.
Z6wXoG8fZ1oYJYpH0v8gG0Z7b5rBZQ7lQ5k6dafV8d0X0g"""
            }
        }
