from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

# custom import(s)
from app.db.database import get_db
from app.schemas.db_schema import EndPointCall

metric_router = APIRouter()


# metric endpoint
@metric_router.get("/metrics", response_model=EndPointCall, tags=["Metrics"])
async def get_all_calls(db: Session = Depends(get_db)):
    """
    function to calculate the metrics
    Args:
        db: Session
    Return:
        dictionary
    """
    try:
        query_latency = text("""
            SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY call_latency) AS med_val
            FROM endpoint_calls;
        """)
        result_latency = db.execute(query_latency)
        median_value_latency = result_latency.scalar()

        query_length = text("""
            SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY length) AS med_len
            FROM endpoint_calls;
        """)
        result_length = db.execute(query_length)
        median_value_length = result_length.scalar()

        query_calls = text("""
            SELECT MAX(id) FROM endpoint_calls;
        """)
        result_calls = db.execute(query_calls)
        total_calls = result_calls.scalar()

        return JSONResponse(
            content={
                "median_latency": median_value_latency,
                "median_audio_length": median_value_length,
                "total_no_of_calls": total_calls,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
