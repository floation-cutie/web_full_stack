from sqlalchemy.orm import Session
from app.models.service_response import ServiceResponse
from app.models.service_request import ServiceRequest
from app.models.user import BUser
from app.models.accept_info import AcceptInfo
from app.schemas.service_response import ServiceResponseCreate, ServiceResponseUpdate
from math import ceil

def get_service_response(db: Session, response_id: int):
    return db.query(ServiceResponse).filter(ServiceResponse.response_id == response_id).first()

def get_service_response_with_details(db: Session, response_id: int):
    """Get service response with responder details if accepted"""
    response = db.query(ServiceResponse).filter(ServiceResponse.response_id == response_id).first()
    if not response:
        return None
    
    # Convert to dict to add additional fields
    response_dict = response.__dict__.copy()
    
    print(f"DEBUG: Initial response data: {response_dict}")
    print(f"DEBUG: Response state: {response.response_state}")
    
    # If response is accepted, get responder information
    if response.response_state == 1:  # Accepted
        print("DEBUG: Response is accepted, looking for accept info...")
        # Get accept info with responder details
        accept_info = db.query(AcceptInfo).filter(
            AcceptInfo.response_id == response.response_id
        ).first()
        
        print(f"DEBUG: Accept info found: {accept_info}")
        
        if accept_info and accept_info.responder:
            print(f"DEBUG: Responder found: {accept_info.responder}")
            response_dict['responder_name'] = accept_info.responder.uname
            response_dict['responder_phone'] = accept_info.responder.phoneNo
            print(f"DEBUG: Added responder info - name: {accept_info.responder.uname}, phone: {accept_info.responder.phoneNo}")
    
    # Remove SQLAlchemy internal attributes
    response_dict.pop('_sa_instance_state', None)
    
    # Debug print
    print(f"DEBUG: get_service_response_with_details returning: {response_dict}")
    return response_dict

def get_service_responses(db: Session, page: int = 1, size: int = 10, user_id: int = None,
                          sr_id: int = None, response_state: int = None, city_id: int = None):
    # Base query for service responses
    # Join with ServiceRequest to enable city filtering
    query = db.query(ServiceResponse).join(ServiceRequest, ServiceResponse.sr_id == ServiceRequest.sr_id)

    if user_id is not None:
        query = query.filter(ServiceResponse.response_userid == user_id)
    if sr_id is not None:
        query = query.filter(ServiceResponse.sr_id == sr_id)
    if response_state is not None:
        query = query.filter(ServiceResponse.response_state == response_state)
    if city_id is not None:
        query = query.filter(ServiceRequest.cityID == city_id)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    # Enhance items with responder information if they are accepted
    enhanced_items = []
    for item in items:
        # Convert to dict to add additional fields
        item_dict = item.__dict__.copy()
        
        print(f"DEBUG: Processing item - ID: {item.response_id}, State: {item.response_state}")
        
        # If response is accepted, get responder information
        if item.response_state == 1:  # Accepted
            print("DEBUG: Item is accepted, looking for accept info...")
            # Join with AcceptInfo to get responder details
            accept_info = db.query(AcceptInfo).filter(
                AcceptInfo.response_id == item.response_id
            ).first()
            
            print(f"DEBUG: Accept info found for item: {accept_info}")
            
            if accept_info and accept_info.responder:
                print(f"DEBUG: Responder found for item: {accept_info.responder}")
                item_dict['responder_name'] = accept_info.responder.uname
                item_dict['responder_phone'] = accept_info.responder.phoneNo
                print(f"DEBUG: Added responder info for item - name: {accept_info.responder.uname}, phone: {accept_info.responder.phoneNo}")
        else:
            # For non-accepted responses, still include responder info from the response user
            # This helps with debugging and showing who responded
            responder = db.query(BUser).filter(BUser.id == item.response_userid).first()
            if responder:
                item_dict['responder_name'] = responder.uname
                item_dict['responder_phone'] = responder.phoneNo
        
        # Remove SQLAlchemy internal attributes
        item_dict.pop('_sa_instance_state', None)
        enhanced_items.append(item_dict)
    
    return {
        "items": enhanced_items,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": ceil(total / size) if size > 0 else 0
    }

def create_service_response(db: Session, response: ServiceResponseCreate, user_id: int):
    db_response = ServiceResponse(
        **response.model_dump(),
        response_userid=user_id
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def update_service_response(db: Session, response_id: int, response_update: ServiceResponseUpdate):
    db_response = get_service_response(db, response_id)
    if not db_response:
        return None
    
    update_data = response_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_response, field, value)
    
    db.commit()
    db.refresh(db_response)
    return db_response

def delete_service_response(db: Session, response_id: int):
    db_response = get_service_response(db, response_id)
    if not db_response:
        return False
    
    db.delete(db_response)
    db.commit()
    return True

def has_responses(db: Session, request_id: int) -> bool:
    """
    Check if a service request has any responses.
    
    Args:
        db: Database session
        request_id: Service request ID to check
        
    Returns:
        bool: True if the service request has any responses, False otherwise
    """
    count = db.query(ServiceResponse).filter(ServiceResponse.sr_id == request_id).count()
    return count > 0
