from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.crud import accept as crud_accept
from app.crud.service_response import get_service_response
from app.crud.service_request import get_service_request

router = APIRouter()

@router.post("/accept/{response_id}")
def accept_service(
    response_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_response = get_service_response(db, response_id)
    if not db_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service response not found"
        )
    
    db_request = get_service_request(db, db_response.sr_id)
    if db_request.psr_userid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to accept this response"
        )
    
    if db_response.response_state != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Response already processed"
        )
    
    accept_info = crud_accept.accept_service_response(db, response_id)
    
    return {
        "code": 200,
        "message": "Service response accepted successfully",
        "data": {"accept_id": accept_info.id}
    }

@router.post("/reject/{response_id}")
def reject_service(
    response_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_response = get_service_response(db, response_id)
    if not db_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service response not found"
        )
    
    db_request = get_service_request(db, db_response.sr_id)
    if db_request.psr_userid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to reject this response"
        )
    
    if db_response.response_state != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Response already processed"
        )
    
    updated_response = crud_accept.reject_service_response(db, response_id)
    
    return {
        "code": 200,
        "message": "Service response rejected successfully"
    }
