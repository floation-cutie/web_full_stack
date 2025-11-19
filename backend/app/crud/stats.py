from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.service_request import ServiceRequest
from app.models.accept_info import AcceptInfo
from datetime import datetime

def get_monthly_statistics(
    db: Session,
    start_month: str,
    end_month: str,
    city_id: int = None,
    service_type_id: int = None,
    page: int = 1,
    size: int = 10
):
    start_date = datetime.strptime(f"{start_month}-01", "%Y-%m-%d")
    end_date = datetime.strptime(f"{end_month}-01", "%Y-%m-%d")

    # Detect database type and use appropriate date formatting
    db_dialect = db.bind.dialect.name
    if db_dialect == 'sqlite':
        # SQLite uses strftime
        date_format_func = lambda col: func.strftime('%Y-%m', col)
    else:
        # MySQL uses date_format
        date_format_func = lambda col: func.date_format(col, '%Y-%m')

    needs_query = db.query(
        date_format_func(ServiceRequest.ps_begindate).label('month'),
        func.count(ServiceRequest.id).label('published_count')
    ).filter(
        ServiceRequest.ps_begindate >= start_date,
        ServiceRequest.ps_begindate <= end_date
    )

    if city_id:
        needs_query = needs_query.filter(ServiceRequest.cityID == city_id)
    if service_type_id:
        needs_query = needs_query.filter(ServiceRequest.stype_id == service_type_id)

    needs_query = needs_query.group_by('month')

    completed_query = db.query(
        date_format_func(AcceptInfo.accept_date).label('month'),
        func.count(AcceptInfo.id).label('completed_count')
    ).filter(
        AcceptInfo.accept_date >= start_date,
        AcceptInfo.accept_date <= end_date
    )
    
    needs_data = {row.month: row.published_count for row in needs_query.all()}
    completed_data = {row.month: row.completed_count for row in completed_query.all()}
    
    months = []
    current = start_date
    while current <= end_date:
        month_str = current.strftime('%Y-%m')
        months.append(month_str)
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    
    chart_data = {
        "months": months,
        "published": [needs_data.get(m, 0) for m in months],
        "completed": [completed_data.get(m, 0) for m in months]
    }
    
    table_items = [
        {
            "month": m,
            "publishedCount": needs_data.get(m, 0),
            "completedCount": completed_data.get(m, 0)
        }
        for m in months
    ]
    
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_items = table_items[start_idx:end_idx]
    
    return {
        "chart_data": chart_data,
        "items": paginated_items,
        "total": len(table_items),
        "page": page,
        "size": size
    }
