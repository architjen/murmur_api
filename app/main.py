from fastapi import FastAPI

# custom import(s)
from .api.routes import router

app = FastAPI(title="Faster Whisperers 🐍")

# Set up routes
app.include_router(router)
