from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin
from app.crud import user as crud_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    if crud_user.get_user_by_username(db, user.uname):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = crud_user.create_user(db, user)

    return {
        "code": 200,
        "message": "Registration successful",
        "data": {"user_id": new_user.id}
    }

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_access_token(data={"sub": str(user.id), "username": user.uname})

    return {
        "code": 200,
        "message": "Login successful",
        "data": {
            "token": token,
            "user_info": {
                "id": user.id,
                "uname": user.uname,
                "bname": user.bname,
                "phoneNo": user.phoneNo
            }
        }
    }
