from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.service_request import ServiceRequestCreate, ServiceRequestUpdate, ServiceRequestResponse
from app.crud import service_request as crud_service_request
from app.crud import service_response as crud_service_response

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
    # Log the received parameters for debugging
    print(f"get_service_requests called with params: page={page}, size={size}, user_id={user_id}, stype_id={stype_id}, city_id={city_id}, ps_state={ps_state}")
    
    result = crud_service_request.get_service_requests(
        db, page=page, size=size, user_id=user_id,
        stype_id=stype_id, city_id=city_id, ps_state=ps_state
    )
    
    # Convert items to dictionaries and include publisher name and city name
    items_with_details = []
    for item in result["items"]:
        # Convert the SQLAlchemy model object to a dictionary
        item_dict = {}
        for column in item.__table__.columns:
            item_dict[column.name] = getattr(item, column.name)
        
        # Add publisher name (using uname instead of bname)
        if hasattr(item, 'user') and item.user:
            item_dict['publisher_name'] = item.user.uname
        else:
            # If user relationship is not loaded, query for the user name
            from app.models.user import BUser
            user = db.query(BUser).filter(BUser.id == item.psr_userid).first()
            item_dict['publisher_name'] = user.uname if user else 'Unknown'
        
        # Add city name
        if hasattr(item, 'city') and item.city:
            item_dict['city_name'] = item.city.cityName
        else:
            # If city relationship is not loaded, query for the city name
            from app.models.city_info import CityInfo
            city = db.query(CityInfo).filter(CityInfo.cityID == item.cityID).first()
            item_dict['city_name'] = city.cityName if city else 'Unknown'
        
        items_with_details.append(item_dict)

    result["items"] = items_with_details

    return {
        "code": 200,
        "data": result
    }

@router.get("/my")
def get_my_service_requests(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    stype_id: int = Query(None),
    city_id: int = Query(None),
    ps_state: int = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = crud_service_request.get_service_requests(
        db, page=page, size=size, user_id=current_user.id,
        stype_id=stype_id, city_id=city_id, ps_state=ps_state
    )

    return {
        "code": 200,
        "data": result
    }

@router.get("/{request_id}", response_model=dict)
def get_service_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    print(f"Getting service request with ID: {request_id}")
    print(f"Current user ID: {current_user.id}")
    db_request = crud_service_request.get_service_request(db, request_id)
    print(f"DB request found: {db_request is not None}")
    if db_request:
        print(f"DB request data: {db_request.__dict__}")
        print(f"Request owner ID: {db_request.psr_userid}")
        print(f"File list in DB: {db_request.file_list}")
    if not db_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )

    # Convert the SQLAlchemy model object to a dictionary
    request_dict = {}
    for column in db_request.__table__.columns:
        request_dict[column.name] = getattr(db_request, column.name)
    
    # Add publisher name if user relationship is loaded (using uname instead of bname)
    if hasattr(db_request, 'user') and db_request.user:
        request_dict['publisher_name'] = db_request.user.uname
    else:
        # If user relationship is not loaded, query for the user name
        from app.models.user import BUser
        user = db.query(BUser).filter(BUser.id == db_request.psr_userid).first()
        request_dict['publisher_name'] = user.uname if user else 'Unknown'
    
    # Add service type name if service_type relationship is loaded
    if hasattr(db_request, 'service_type') and db_request.service_type:
        request_dict['service_type_name'] = db_request.service_type.typename
    else:
        # If service_type relationship is not loaded, query for the service type name
        from app.models.service_type import ServiceType
        service_type = db.query(ServiceType).filter(ServiceType.id == db_request.stype_id).first()
        request_dict['service_type_name'] = service_type.typename if service_type else 'Unknown'
    
    print(f"Returning request data: {request_dict}")
    return {
        "code": 200,
        "data": request_dict
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
        "data": {"sr_id": db_request.sr_id}
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

    # Check if the service request has any responses
    if crud_service_response.has_responses(db, request_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify a request that has responses"
        )

    updated_request = crud_service_request.update_service_request(db, request_id, request_update)

    return {
        "code": 200,
        "message": "Service request updated successfully",
        "data": updated_request
    }

@router.put("/{request_id}/cancel")
def cancel_service_request(
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
            detail="Not authorized to cancel this request"
        )

    db_request.ps_state = -1
    db.commit()
    db.refresh(db_request)

    return {
        "code": 200,
        "message": "Service request cancelled successfully",
        "data": db_request
    }

@router.get("/{request_id}/responses")
def get_service_request_responses(
    request_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if service request exists
    db_request = crud_service_request.get_service_request(db, request_id)
    if not db_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found"
        )

    # Get responses for this service request
    result = crud_service_response.get_service_responses(
        db, page=page, size=size, sr_id=request_id
    )
    
    # Import the schema for serialization
    from app.schemas.service_response import ServiceResponseResponse
    
    # Validate and serialize each item in the result using the schema
    serialized_items = [ServiceResponseResponse(**item).model_dump() for item in result["items"]]
    result["items"] = serialized_items

    return {
        "code": 200,
        "data": result
    }

@router.delete("/{request_id}")
def delete_service_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
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

        # Create a copy of the request data before deletion
        request_data = {}
        for column in db_request.__table__.columns:
            request_data[column.name] = getattr(db_request, column.name)

        result = crud_service_request.delete_service_request(db, request_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete service request"
            )

        return {
            "code": 200,
            "message": "Service request deleted successfully",
            "data": request_data
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error and raise a 500 error
        print(f"Error deleting service request {request_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
