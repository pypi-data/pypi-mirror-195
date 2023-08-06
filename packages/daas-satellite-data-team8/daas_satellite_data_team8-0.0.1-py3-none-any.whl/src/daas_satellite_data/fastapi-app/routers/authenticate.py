from http.client import HTTPException
from fastapi import APIRouter, Depends, status,HTTPException
from pytest import Session
from hashing import Hash
import schema, db_model,userdb, JWTToken
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(userdb.get_db)):
    """Function to query username and password from the SQLite database to verify Users during
        login and generate JWT Token for the session. Raises 404 Exception if the credentials dont match
    -----
    Input parameters:
    OAuth2PasswordRequestForm : class
        class dependency containing user and password form
    Session : db
        current session of db
    -----
    Returns:
    A string containing the JWT access token and throws a HTTP_404_NOT_FOUND exception in case of error in username/password
    """
    user = db.query(db_model.User_Table).filter(db_model.User_Table.username == request.username).first()  #query to db to match usernames
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invalid Credentials") 

    if not Hash.verify(user.password, request.password):
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Incorrect Password")  #verify hashed password with plain text

    #generate JWT Token
    access_token = JWTToken.create_access_token(data={"sub": user.name})  #generate access token
    return {"access_token": access_token, "token_type": "bearer"}