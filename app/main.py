from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1 import users, records, dashboard
from app.exceptions.app_exception import AppException
from app.utils.logger import get_logger
from app.core.database import engine, Base

logger = get_logger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API", version="1.0.0")

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException: {exc.message} (status={exc.status_code})")
    return JSONResponse(status_code=exc.status_code, content={"success": False, "error": exc.message})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(status_code=500, content={"success": False, "error": "Internal server error"})

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    return response

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(records.router, prefix="/records", tags=["Records"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"success": True, "message": "Finance Dashboard API"}
