from fastapi import FastAPI

# custom import(s)
from .api.routes import router
from .api.metrics import metric_router

app = FastAPI(title="Faster Whisperers 🐍")

# Set up routes
app.include_router(router)

# adding metrics endpoints
app.include_router(metric_router)
