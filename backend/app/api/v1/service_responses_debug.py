import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.service_response import ServiceResponseCreate, ServiceResponseUpdate, ServiceResponseResponse
from app.crud import service_response as crud_service_response
from typing import List

router = APIRouter()

@router.get("/my", response_model=dict)
def get_my_service_responses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get current user's service responses"""
    logger.debug(f"Getting service responses for user {current_user.id}")
    result = crud_service_response.get_service_responses(
        db, page=page, size=size, user_id=current_user.id
    )
    logger.debug(f"CRUD result: {result}")
    
    # Validate and serialize each item in the result using the schema
    serialized_items = [ServiceResponseResponse(**item).model_dump() for item in result["items"]]
    result["items"] = serialized_items
    logger.debug(f"Serialized result: {result}")

    return {
        "code": 200,
        "data": result
    }

@router.get("/{response_id}", response_model=dict)
def get_service_response_by_id(
    response_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific service response by ID"""
    logger.debug(f"Getting service response {response_id}")
    db_response = crud_service_response.get_service_response_with_details(db, response_id)
    logger.debug(f"CRUD response: {db_response}")
    if not db_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service response not found"
        )

    # Validate and serialize the response using the schema
    response_data = ServiceResponseResponse(**db_response)
    logger.debug(f"Validated response: {response_data.model_dump()}")

    return {
        "code": 200,
        "data": response_data.model_dump()
    }

@router.get("", response_model=dict)
def get_service_responses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    user_id: int = Query(None),
    sr_id: int = Query(None),
    response_state: int = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    logger.debug(f"Getting service responses with filters: user_id={user_id}, sr_id={sr_id}, response_state={response_state}")
    result = crud_service_response.get_service_responses(
        db, page=page, size=size, user_id=user_id,
        sr_id=sr_id, response_state=response_state
    )
    logger.debug(f"CRUD result: {result}")
    
    # Validate and serialize each item in the result using the schema
    serialized_items = [ServiceResponseResponse(**item).model_dump() for item in result["items"]]
    result["items"] = serialized_items
    logger.debug(f"Serialized result: {result}")

    return {
        "code": 200,
        "data": result
    }

# ... rest of the code remains the same