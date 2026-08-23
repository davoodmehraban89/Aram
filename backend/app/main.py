from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging

from backend.app.config import settings
from backend.app.api.endpoints import router as api_router
from backend.app.export.endpoints import router as export_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("aram_platform")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Global Error: {exc} at path {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "خطای غیرمنتظره در سرور رخ داده است. لطفاً مجدداً تلاش کنید.",
            "error_type": type(exc).__name__,
        },
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(export_router, prefix=settings.API_V1_STR)

@app.get("/info")
def root_info():
    return {"message": "Financial Reporting Platform API Foundation", "docs": "/docs"}

# Serve desktop static frontend assets
app.mount("/", StaticFiles(directory="desktop/static", html=True), name="desktop_static")
