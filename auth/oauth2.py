from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from fastapi.param_functions import Depends
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from db import db_user
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 
key = os.environ.get('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now() + expires_delta
  else:
    expire = datetime.now() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, key, algorithm=ALGORITHM)
  return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
       status_code=status.HTTP_401_UNAUTHORIZED,
       detail="Coul not validate credentials",
       headers={"WWW-Authenticate": "Bearer"}
    )
    try:
       payload = jwt.decode(token, key, algorithms=[ALGORITHM])
       username: str = payload.get('sub')
       if username is None:
          raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db_user.get_user_by_username(db, username)

    if user is None:
       raise credentials_exception
    
    return user