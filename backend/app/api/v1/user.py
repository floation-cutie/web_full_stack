from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.user import UserResponse, UserUpdate, PasswordUpdate
from app.crud import user as crud_user
from app.core.security import verify_password

router = APIRouter()

@router.get("/me")
def get_current_user_info(current_user = Depends(get_current_user)):
    return {
        "code": 200,
        "data": current_user
    }

@router.put("/me")
def update_current_user(
    user_update: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = crud_user.update_user(db, current_user.id, user_update)

    return {
        "code": 200,
        "message": "User updated successfully",
        "data": updated_user
    }

@router.put("/me/password")
def update_password(
    password_update: PasswordUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_update.old_password, current_user.bpwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
    
    crud_user.update_password(db, current_user.id, password_update.new_password)
    
    return {
        "code": 200,
        "message": "Password updated successfully"
    }
