from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.crud import stats as crud_stats
from app.models.city_info import CityInfo

router = APIRouter()

@router.get("/monthly")
def get_monthly_statistics(
    start_month: str = Query(..., description="Start month in YYYY-MM format"),
    end_month: str = Query(..., description="End month in YYYY-MM format"),
    city_id: int = Query(None, description="Filter by city ID"),
    city_name: str = Query(None, description="Filter by city name"),
    service_type_id: int = Query(None, description="Filter by service type ID"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # If city_name is provided, find the corresponding city_id
    if city_name:
        city = db.query(CityInfo).filter(CityInfo.cityName == city_name).first()
        if city:
            city_id = city.cityID
        else:
            city_id = None  # No matching city found
    
    result = crud_stats.get_monthly_statistics(
        db, start_month, end_month, city_id, service_type_id, page, size
    )
    
    return {
        "code": 200,
        "data": result
    }
