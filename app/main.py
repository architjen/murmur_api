from fastapi import FastAPI, UploadFile, HTTPException, File, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import asyncio
from typing import Dict
import os
from faster_whisper import WhisperModel
import time

# custom import(s)
from .api.metrics import metric_router
from app.db.database import get_db
from app.db import crud

from app.models import db_model
from app.schemas import db_schema

#db_dependency = Annotated[Session, Depends(get_db)]
app = FastAPI(title="Faster Whisperers Queue 🐍")

queue = asyncio.Queue()

# redirecting the localhost to /docs directly
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"


# an endpoint to test
@app.get("/ping")
def hello():
    return {"msg": "Hello world"}


def transcribe_audio(temp_file):
    """ the function to transcribe the audio"""
    start_time = time.time()
    
    model = WhisperModel("base", device="cpu", compute_type="int8")
    # result is a generator here
    result, info = model.transcribe(temp_file)
    latency = time.time() - start_time
    
    return " ".join(segment.text for segment in result), latency, info.duration


# the endpoint for transcribe
@app.post("/transcribe")
async def transcribe(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["audio/mpeg", "audio/wav", "audio/mp3"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = f"audio_.wav"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Add the task to the queue to be processed by a worker
    await queue.put(file_path)  # Put task into the queue

    # Start background task to process the queue
    background_tasks.add_task(process_queue, db)

    return {"message": "Audio file is being processed"}

async def process_queue(db: Session):
    """Worker that processes tasks in the queue"""
    while not queue.empty():
        file_path = await queue.get()  # Get the task from the queue
        
        content, call_latency, duration = transcribe_audio(file_path)

        # After transcription, create a record in the database
        new_task = db_model.EndPointCall(
            content=content,
            call_latency=call_latency,
            length=duration
        )

        # Add task to DB
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        # Clean up the saved file after processing
        os.remove(file_path)
        
        print(f"Task transcription completed!")
        

@app.get("/all_data", response_model=list[db_schema.EndPointCall])
async def get_all_calls(db: Session = Depends(get_db)):
    return crud.get_endpointcalls(db)

# adding metrics endpoints
app.include_router(metric_router)
