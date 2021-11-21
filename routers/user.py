from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from database import database, models
from schemas.user import UserCreate, UserResponse
from security import utils

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_users(user: UserCreate, db: Session = Depends(database.get_db)):
    user.password = utils.hash_password(user.password)

    user_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user.email}' already exists",
        )

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found",
        )
    return user
