from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.service_request import ServiceRequest
from app.models.accept_info import AcceptInfo
from datetime import datetime, timedelta

def get_monthly_statistics(
    db: Session,
    start_month: str,
    end_month: str,
    city_id: int = None,
    service_type_id: int = None,
    page: int = 1,
    size: int = 10
):
    # Parse start date as first day of the month
    start_date = datetime.strptime(f"{start_month}-01", "%Y-%m-%d")
    
    # Parse end date as last day of the month
    end_year, end_month_num = map(int, end_month.split('-'))
    if end_month_num == 12:
        end_year += 1
        end_month_num = 1
    else:
        end_month_num += 1
    end_date = datetime(end_year, end_month_num, 1) - timedelta(days=1)

    # Detect database type and use appropriate date formatting
    db_dialect = db.bind.dialect.name
    if db_dialect == 'sqlite':
        # SQLite uses strftime
        date_format_func = lambda col: func.strftime('%Y-%m', col)
    else:
        # MySQL uses date_format
        date_format_func = lambda col: func.date_format(col, '%Y-%m')

    # Build base needs query with filters
    needs_query = db.query(
        date_format_func(ServiceRequest.ps_begindate).label('month'),
        func.count(ServiceRequest.sr_id).label('published_count')
    ).filter(
        ServiceRequest.ps_begindate >= start_date,
        ServiceRequest.ps_begindate <= end_date
    )

    # Apply optional filters
    if city_id:
        needs_query = needs_query.filter(ServiceRequest.cityID == city_id)
    if service_type_id:
        needs_query = needs_query.filter(ServiceRequest.stype_id == service_type_id)

    needs_query = needs_query.group_by('month')

    # Build completed services query by joining with ServiceRequest to ensure 
    # completed services are only counted if they correspond to published needs
    completed_query = db.query(
        date_format_func(AcceptInfo.createdate).label('month'),
        func.count(AcceptInfo.id).label('completed_count')
    ).join(
        ServiceRequest, AcceptInfo.srid == ServiceRequest.sr_id
    ).filter(
        AcceptInfo.createdate >= start_date,
        AcceptInfo.createdate <= end_date,
        ServiceRequest.ps_begindate >= start_date,
        ServiceRequest.ps_begindate <= end_date
    )
    
    # Apply same optional filters to completed query
    if city_id:
        completed_query = completed_query.filter(ServiceRequest.cityID == city_id)
    if service_type_id:
        completed_query = completed_query.filter(ServiceRequest.stype_id == service_type_id)
        
    completed_query = completed_query.group_by('month')
    
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
