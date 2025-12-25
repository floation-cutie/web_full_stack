from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_access_token
from app.models.user import BUser

# 设置日志
logger = logging.getLogger(__name__)

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> BUser:
    try:
        logger.info("验证用户身份")
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication credentials"
            )
            
        token = credentials.credentials
        logger.info(f"Token: {token[:10]}...")  # 只记录前10个字符
        
        payload = decode_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        user_id_int = int(user_id)
        
        # If user_id is 0, this is the admin user (dummy user created during authentication)
        if user_id_int == 0:
            # Check if this is actually an admin by looking up in auser_table
            from sqlalchemy import text
            admin_result = db.execute(
                text("SELECT aname, apwd FROM auser_table WHERE aname = 'admin'") 
            ).fetchone()
            
            if admin_result:
                # Create a dummy BUser object for the admin user
                dummy_user = BUser(
                    id=0,
                    uname=admin_result.aname,
                    bname=admin_result.aname,
                    phoneNo="",
                    ctype="admin",
                    idno="admin",
                    bpwd=admin_result.apwd,
                    rdate=None,
                    userlvl="admin"
                )
                logger.info(f"Admin user validated: {dummy_user.uname}")
                return dummy_user
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Admin user not found"
                )
        
        user = db.query(BUser).filter(BUser.id == user_id_int).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        logger.info(f"用户验证成功: {user.id}")
        return user
    except HTTPException as he:
        logger.error(f"认证HTTP错误: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"认证过程中发生未知错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}"
        )

def get_current_admin(
    current_user: BUser = Depends(get_current_user)
):
    if getattr(current_user, 'userlvl', None) != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
