from sqlalchemy.orm import Session
from app.models.accept_info import AcceptInfo
from app.models.service_response import ServiceResponse

def accept_service_response(db: Session, response_id: int):
    db_response = db.query(ServiceResponse).filter(ServiceResponse.response_id == response_id).first()
    if not db_response:
        return None

    db_response.response_state = 1

    # Get the service request to extract publisher info
    from app.models.service_request import ServiceRequest
    db_request = db.query(ServiceRequest).filter(ServiceRequest.sr_id == db_response.sr_id).first()

    db_accept = AcceptInfo(
        response_id=response_id,
        srid=db_response.sr_id,
        psr_userid=db_request.psr_userid,
        response_userid=db_response.response_userid
    )
    db.add(db_accept)

    db.commit()
    db.refresh(db_accept)
    return db_accept

def reject_service_response(db: Session, response_id: int):
    db_response = db.query(ServiceResponse).filter(ServiceResponse.response_id == response_id).first()
    if not db_response:
        return None

    db_response.response_state = 2
    db.commit()
    db.refresh(db_response)
    return db_response
