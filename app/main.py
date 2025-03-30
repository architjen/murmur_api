from fastapi import FastAPI

# custom import(s)
from .api.routes import router
from .api.metrics import metric_router

app = FastAPI(title="Faster Whisperers 🐍")

# Adding transcribe and get_data endpoints
app.include_router(router)

# adding metrics endpoint
app.include_router(metric_router)
