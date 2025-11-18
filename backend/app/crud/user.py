from sqlalchemy.orm import Session
from app.models.user import BUser
from app.schemas.auth import UserRegister
from app.schemas.user import UserUpdate
from app.core.security import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(BUser).filter(BUser.uname == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(BUser).filter(BUser.id == user_id).first()

def create_user(db: Session, user: UserRegister):
    hashed_password = get_password_hash(user.bpwd)
    db_user = BUser(
        uname=user.uname,
        ctype=user.ctype,
        idno=user.idno,
        bname=user.bname,
        bpwd=hashed_password,
        phoneNo=user.phoneNo,
        desc=user.desc
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.bpwd):
        return None
    return user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, user_id: int, new_password: str):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.bpwd = get_password_hash(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user
