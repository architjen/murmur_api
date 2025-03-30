from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session

# custom import(s)
from app.schemas.transcription import TranscriptionResponse
from app.models.whisper_model import transcribe_audio
from app.db.database import get_db
from app.db import crud
from app.schemas import db_schema

router = APIRouter()


# redirecting the localhost to /docs directly
@router.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"


# an endpoint to test
@router.get("/ping", tags=["Ping"])
def hello():
    return {"msg": "Hello world"}


# the endpoint for transcribe
@router.post(
    "/transcribe", response_model=TranscriptionResponse, tags=["Transcribe Audio"]
)
async def transcribe(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["audio/mpeg", "audio/wav", "audio/mp3", "audio/x-wav"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    try:
        # function call to the faster-whisper function
        text, latency, duration = await transcribe_audio(file)
        # add values to db after parsing through pydantic
        crud.create_endpointcall(
            db,
            db_schema.EndPointCallCreate(
                content=text, call_latency=latency, length=duration
            ),
        )
        return JSONResponse(content={"text": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# gets all the data
@router.get("/get_data", response_model=list[db_schema.EndPointCall], tags=["Data"])
async def get_all_calls(db: Session = Depends(get_db)):
    return crud.get_endpointcalls(db)
