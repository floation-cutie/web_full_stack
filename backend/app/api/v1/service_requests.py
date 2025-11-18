from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.service_request import ServiceRequestCreate, ServiceRequestUpdate, ServiceRequestResponse
from app.crud import service_request as crud_service_request

router = APIRouter()

@router.get("")
def get_service_requests(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    user_id: int = Query(None),
    stype_id: int = Query(None),
    city_id: int = Query(None),
    ps_state: int = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = crud_service_request.get_service_requests(
        db, page=page, size=size, user_id=user_id, 
        stype_id=stype_id, city_id=city_id, ps_state=ps_state
    )
    
    return {
        "code": 200,
        "data": result
    }

@router.post("", status_code=status.HTTP_201_CREATED)
def create_service_request(
    request: ServiceRequestCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_request = crud_service_request.create_service_request(db, request, current_user.id)
    
    return {
        "code": 200,
        "message": "Service request created successfully",
        "data": {"id": db_request.id}
    }

@router.put("/{request_id}")
def update_service_request(
    request_id: int,
    request_update: ServiceRequestUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_request = crud_service_request.get_service_request(db, request_id)
    if not db_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )
    
    if db_request.psr_userid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this request"
        )
    
    updated_request = crud_service_request.update_service_request(db, request_id, request_update)
    
    return {
        "code": 200,
        "message": "Service request updated successfully",
        "data": {"id": updated_request.id}
    }

@router.delete("/{request_id}")
def delete_service_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_request = crud_service_request.get_service_request(db, request_id)
    if not db_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )
    
    if db_request.psr_userid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this request"
        )
    
    crud_service_request.delete_service_request(db, request_id)
    
    return {
        "code": 200,
        "message": "Service request deleted successfully"
    }
