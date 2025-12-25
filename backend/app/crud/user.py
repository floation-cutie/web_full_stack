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
    # 首先检查普通用户表
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.bpwd):
        return user
    
    # 如果在普通用户表中未找到，检查管理员表
    from sqlalchemy import text
    admin_result = db.execute(
        text("SELECT aname, apwd FROM auser_table WHERE aname = :username"), 
        {"username": username}
    ).fetchone()
    
    if admin_result:
        # 验证管理员密码（假设管理员密码未加密存储）
        if password == admin_result.apwd:
            # 创建一个虚拟的BUser对象用于返回
            # 这样可以保持API的一致性
            dummy_user = BUser(
                id=0,  # 管理员ID设置为0或使用其他标识
                uname=admin_result.aname,
                bname=admin_result.aname,  # 使用用户名作为姓名
                phoneNo="",  # 管理员电话号码为空
                ctype="admin",  # 设置为管理员类型
                idno="admin",  # 设置为admin
                bpwd=admin_result.apwd,  # 密码
                rdate=None,  # 注册日期为空
                userlvl="admin"  # 设置用户级别为admin
            )
            return dummy_user
    
    return None

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
