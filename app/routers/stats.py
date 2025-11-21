from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database import get_db
from app.models.indicator import Indicator
from app.core.config import get_current_user
from app.models.user import User

router = APIRouter()

# =========================
# 1) Moyennes /stats/air/averages
# Exemple TP:
# /stats/air/averages?from=yyyy-mm-dd&to=yyyy-mm-dd&zone=...
# =========================
@router.get("/air/averages")
def air_averages(
    db: Session = Depends(get_db),
    __: User = Depends(get_current_user),
    from_date: datetime = Query(..., alias="from"),
    to_date: datetime = Query(..., alias="to"),
    zone_id: int | None = Query(None, alias="zone"),
):
    q = db.query(func.avg(Indicator.value)).filter(Indicator.type == "air")
    q = q.filter(Indicator.timestamp >= from_date, Indicator.timestamp <= to_date)
    if zone_id:
        q = q.filter(Indicator.zone_id == zone_id)

    avg_val = q.scalar()
    if avg_val is None:
        return {"labels": [], "series": []}

    return {
        "labels": ["air"],
        "series": [round(float(avg_val), 3)]
    }

# =========================
# 2) Tendances /stats/co2/trend
# Exemple TP:
# /stats/co2/trend?zone=...&period=monthly
# =========================
@router.get("/co2/trend")
def co2_trend(
    db: Session = Depends(get_db),
    __: User = Depends(get_current_user),
    zone_id: int | None = Query(None, alias="zone"),
    period: str = Query("daily", pattern="^(daily|monthly)$"),
):
    # SQLite: group by date avec strftime
    if period == "monthly":
        bucket = func.strftime("%Y-%m", Indicator.timestamp)
    else:
        bucket = func.strftime("%Y-%m-%d", Indicator.timestamp)

    q = db.query(
        bucket.label("bucket"),
        func.avg(Indicator.value).label("avg_value")
    ).filter(Indicator.type == "co2")

    if zone_id:
        q = q.filter(Indicator.zone_id == zone_id)

    q = q.group_by("bucket").order_by("bucket")

    rows = q.all()
    labels = [r.bucket for r in rows]
    series = [round(float(r.avg_value), 3) for r in rows]

    return {"labels": labels, "series": series}

# =========================
# 3) Stats génériques (bonus utile)
# /stats/indicator/averages?type=air&zone_id=1&from=...&to=...
# =========================
@router.get("/indicator/averages")
def indicator_averages(
    db: Session = Depends(get_db),
    __: User = Depends(get_current_user),
    type: str = Query(...),
    from_date: datetime = Query(..., alias="from"),
    to_date: datetime = Query(..., alias="to"),
    zone_id: int | None = None,
):
    q = db.query(func.avg(Indicator.value)).filter(Indicator.type == type)
    q = q.filter(Indicator.timestamp >= from_date, Indicator.timestamp <= to_date)
    if zone_id:
        q = q.filter(Indicator.zone_id == zone_id)

    avg_val = q.scalar()
    if avg_val is None:
        return {"labels": [], "series": []}

    return {"labels": [type], "series": [round(float(avg_val), 3)]}
