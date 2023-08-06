from typing import Optional
from pydantic import BaseModel
from unicodedata import name
from click import confirmation_option, password_option
from enum import Enum 

class User(BaseModel):  #class to create or access user 
    name: str
    username : str
    password: str
    plan : str  #added plan assignment 3
    user_type : str

class UpdateUserPassword(BaseModel):
    password : str
    
    class Config():
        orm_mode = True

class ShowUser(BaseModel): #class to show only the name of the user as a response
    name: str

    class Config():
       orm_mode = True  #allows app to take ORM object and translate into responses

class Login(BaseModel): #class for login
    username: str
    password : str

class Token(BaseModel): #token class with access token and token type
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Plan(str, Enum):   #class to show plans as options in CLI
    free = 'free'
    gold = 'gold'
    platinum = 'platinum'