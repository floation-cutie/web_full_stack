from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.service_response import ServiceResponseCreate, ServiceResponseUpdate, ServiceResponseResponse
from app.crud import service_response as crud_service_response

router = APIRouter()

@router.get("/my")
def get_my_service_responses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get current user's service responses"""
    result = crud_service_response.get_service_responses(
        db, page=page, size=size, user_id=current_user.id
    )

    return {
        "code": 200,
        "data": result
    }

@router.get("/{response_id}")
def get_service_response_by_id(
    response_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific service response by ID"""
    db_response = crud_service_response.get_service_response(db, response_id)
    if not db_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service response not found"
        )

    return {
        "code": 200,
        "data": db_response
    }

@router.get("")
def get_service_responses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    user_id: int = Query(None),
    srid: int = Query(None),
    response_state: int = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = crud_service_response.get_service_responses(
        db, page=page, size=size, user_id=user_id,
        srid=srid, response_state=response_state
    )

    return {
        "code": 200,
        "data": result
    }

@router.post("", status_code=status.HTTP_201_CREATED)
def create_service_response(
    response: ServiceResponseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_response = crud_service_response.create_service_response(db, response, current_user.id)
    
    return {
        "code": 200,
        "message": "Service response created successfully",
        "data": {"id": db_response.id}
    }

@router.put("/{response_id}")
def update_service_response(
    response_id: int,
    response_update: ServiceResponseUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_response = crud_service_response.get_service_response(db, response_id)
    if not db_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service response not found"
        )
    
    if db_response.response_userid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this response"
        )
    
    updated_response = crud_service_response.update_service_response(db, response_id, response_update)

    return {
        "code": 200,
        "message": "Service response updated successfully",
        "data": updated_response
    }

@router.put("/{response_id}/cancel")
def cancel_service_response(
    response_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cancel a service response by setting response_state to 3"""
    db_response = crud_service_response.get_service_response(db, response_id)
    if not db_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service response not found"
        )

    if db_response.response_userid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this response"
        )

    # Set response_state to 3 (cancelled)
    db_response.response_state = 3
    db.commit()
    db.refresh(db_response)

    return {
        "code": 200,
        "message": "Service response cancelled successfully",
        "data": db_response
    }

@router.delete("/{response_id}")
def delete_service_response(
    response_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_response = crud_service_response.get_service_response(db, response_id)
    if not db_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service response not found"
        )

    if db_response.response_userid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this response"
        )

    crud_service_response.delete_service_response(db, response_id)

    return {
        "code": 200,
        "message": "Service response deleted successfully",
        "data": db_response
    }
