from sqlalchemy.orm import Session
from app.models.service_response import ServiceResponse
from app.schemas.service_response import ServiceResponseCreate, ServiceResponseUpdate
from math import ceil

def get_service_response(db: Session, response_id: int):
    return db.query(ServiceResponse).filter(ServiceResponse.id == response_id).first()

def get_service_responses(db: Session, page: int = 1, size: int = 10, user_id: int = None,
                          srid: int = None, response_state: int = None):
    query = db.query(ServiceResponse)
    
    if user_id is not None:
        query = query.filter(ServiceResponse.response_userid == user_id)
    if srid is not None:
        query = query.filter(ServiceResponse.srid == srid)
    if response_state is not None:
        query = query.filter(ServiceResponse.response_state == response_state)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return {
        "items": items,
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
    
    db_response.response_state = 3
    db.commit()
    return True
