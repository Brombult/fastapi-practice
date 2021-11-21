from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import database, models
from schemas.token import TokenData
from settings import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def verify_access_token(token: str, cred_exc):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise cred_exc

        token_data = TokenData(id=id)
    except JWTError:
        raise cred_exc

    return token_data


def get_current_user(
    token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)
):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, cred_exc)
    return db.query(models.User).filter(models.User.id == token.id).first()
