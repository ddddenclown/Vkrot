from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.api import router as v1_router
from app.db import engine, Base
import app.models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Unbake API", version="1.0.0")
app.include_router(v1_router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": str(exc), "code": 500},
    )
