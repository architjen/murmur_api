from fastapi import APIRouter, UploadFile, HTTPException, File
from fastapi.responses import RedirectResponse, JSONResponse

# custom import(s)
from app.schemas.transcription import TranscriptionResponse
from app.models.whisper_model import transcribe_audio

router = APIRouter()

# redirecting the localhost to /docs directly
@router.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"

# an endpoint to test
@router.get("/ping")
def hello():
    return {"msg": "Hello world"}

# the endpoint for transcribe
@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    if file.content_type not in ["audio/mpeg", "audio/wav", "audio/mp3"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    try:
        # function call to the faster-whisper function
        text = await transcribe_audio(file)
        return JSONResponse(content={"text": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))