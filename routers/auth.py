from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import database, models
from security import utils, oath
from schemas.token import Token


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)
):
    user_not_found_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
    )

    user = db.query(models.User).filter(models.User.email == creds.username).first()

    if not user:
        raise user_not_found_exception

    if not utils.verify_password(creds.password, user.password):
        raise user_not_found_exception

    access_token = oath.create_access_token({"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
