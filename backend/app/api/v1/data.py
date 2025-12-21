from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.city_info import CityInfo
from app.models.service_type import ServiceType

router = APIRouter()

@router.get("/cities")
def get_cities(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Filter out duplicate English cities (Beijing and Shanghai)
    cities = db.query(CityInfo).filter(
        CityInfo.cityID.notin_([1, 2])  # Exclude Beijing(ID=1) and Shanghai(ID=2)
    ).all()
    return {
        "code": 200,
        "data": [{"id": city.cityID, "name": city.cityName} for city in cities]
    }

@router.get("/service-types")
def get_service_types(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service_types = db.query(ServiceType).all()
    return {
        "code": 200,
        "data": [{"id": st.id, "name": st.typename} for st in service_types]
    }