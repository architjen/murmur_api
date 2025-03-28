from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

# redirecting the localhost to /docs directly
@router.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"

# an endpoint to test
@router.get("/ping")
def hello():
    return {"msg": "Hello world"}