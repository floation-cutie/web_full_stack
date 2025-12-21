from sqlalchemy.orm import Session
from app.models.service_request import ServiceRequest
from app.schemas.service_request import ServiceRequestCreate, ServiceRequestUpdate
from math import ceil
from datetime import datetime

def get_service_request(db: Session, request_id: int):
    return db.query(ServiceRequest).filter(ServiceRequest.sr_id == request_id).first()

def get_service_requests(db: Session, page: int = 1, size: int = 10, user_id: int = None,
                         stype_id: int = None, city_id: int = None, ps_state: int = None):
    # Log the received parameters for debugging
    print(f"CRUD get_service_requests called with params: page={page}, size={size}, user_id={user_id}, stype_id={stype_id}, city_id={city_id}, ps_state={ps_state}")
    
    # Use joinedload to eagerly load relationships
    from sqlalchemy.orm import joinedload
    query = db.query(ServiceRequest).options(
        joinedload(ServiceRequest.user),
        joinedload(ServiceRequest.city),
        joinedload(ServiceRequest.service_type)
    )
    
    if user_id is not None:
        query = query.filter(ServiceRequest.psr_userid == user_id)
        print(f"Applied user_id filter: {user_id}")
    if stype_id is not None:
        query = query.filter(ServiceRequest.stype_id == stype_id)
        print(f"Applied stype_id filter: {stype_id}")
    if city_id is not None:
        query = query.filter(ServiceRequest.cityID == city_id)
        print(f"Applied city_id filter: {city_id}")
    if ps_state is not None:
        query = query.filter(ServiceRequest.ps_state == ps_state)
        print(f"Applied ps_state filter: {ps_state}")

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    print(f"Query result: total={total}, items_count={len(items)}")

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": ceil(total / size) if size > 0 else 0
    }

def create_service_request(db: Session, request: ServiceRequestCreate, user_id: int):
    # Log the incoming request data to debug file_list
    print(f"Creating service request with data: {request.model_dump()}")
    print(f"File list value: {request.file_list}")
    
    db_request = ServiceRequest(
        **request.model_dump(),
        psr_userid=user_id,
        ps_state=0
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    # Log the stored data
    print(f"Stored request ID {db_request.sr_id} with file_list: {db_request.file_list}")
    return db_request

def update_service_request(db: Session, request_id: int, request_update: ServiceRequestUpdate):
    db_request = get_service_request(db, request_id)
    if not db_request:
        return None

    update_data = request_update.model_dump(exclude_unset=True)

    # Always update the ps_updatedate when modifying the request
    if update_data:
        update_data['ps_updatedate'] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_request, field, value)

    db.commit()
    db.refresh(db_request)
    return db_request

def delete_service_request(db: Session, request_id: int):
    try:
        db_request = get_service_request(db, request_id)
        if not db_request:
            return False

        db.delete(db_request)
        db.commit()
        return True
    except Exception as e:
        print(f"Error in delete_service_request: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
