from sqlalchemy.orm import Session
from app.models.service_request import ServiceRequest
from app.schemas.service_request import ServiceRequestCreate, ServiceRequestUpdate
from math import ceil
from datetime import datetime

def get_service_request(db: Session, request_id: int):
    return db.query(ServiceRequest).filter(ServiceRequest.sr_id == request_id).first()

def get_service_requests(db: Session, page: int = 1, size: int = 10, user_id: int = None,
                         stype_id: int = None, city_id: int = None, ps_state: int = None):
    query = db.query(ServiceRequest)

    if user_id is not None:
        query = query.filter(ServiceRequest.psr_userid == user_id)
    if stype_id is not None:
        query = query.filter(ServiceRequest.stype_id == stype_id)
    if city_id is not None:
        query = query.filter(ServiceRequest.cityID == city_id)
    if ps_state is not None:
        query = query.filter(ServiceRequest.ps_state == ps_state)

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": ceil(total / size) if size > 0 else 0
    }

def create_service_request(db: Session, request: ServiceRequestCreate, user_id: int):
    db_request = ServiceRequest(
        **request.model_dump(),
        psr_userid=user_id,
        ps_state=0
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
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
    db_request = get_service_request(db, request_id)
    if not db_request:
        return False

    db_request.ps_state = -1
    db_request.ps_updatedate = datetime.utcnow()
    db.commit()
    return True
