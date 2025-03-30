from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

# custom import(s)
from app.db.database import get_db

metric_router = APIRouter()


@metric_router.get("/metrics")
async def get_all_calls(db: Session = Depends(get_db)):
    query1 = text("""
        SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY call_latency) AS median_value
        FROM endpoint_calls;
    """)
    result1 = db.execute(query1)
    median_value_latency = result1.scalar()

    query2 = text("""
        SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY length) AS median_value
        FROM endpoint_calls;
    """)
    result2 = db.execute(query2)
    median_value_length = result2.scalar()

    query3 = text("""
        SELECT MAX(id) FROM endpoint_calls;
    """)
    result3 = db.execute(query3)
    total_calls = result3.scalar()

    return {
        "median_latency": median_value_latency,
        "median_audio_length": median_value_length,
        "total_no_of_calls": total_calls,
    }
