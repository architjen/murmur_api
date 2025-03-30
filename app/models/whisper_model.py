from faster_whisper import WhisperModel
import tempfile
from fastapi import UploadFile
import time

# create whisper model here
# using cpu based model with int8
# cuda, with float16 could've been used
model = WhisperModel("base", device="cpu", compute_type="int8")


# function that transcribes the audio
async def transcribe_audio(file: UploadFile):
    start_time = time.time()
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    # transcription text along with other meta data
    result, info = model.transcribe(temp_file_path)
    latency = time.time() - start_time
    return " ".join(segment.text for segment in result), latency, info.duration
