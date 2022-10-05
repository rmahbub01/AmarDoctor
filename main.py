from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from doctor.api.api_v1.api import api_router
from doctor.core.config import settings
from doctor.api import deps
from doctor.models.usermodel import User
from doctor.db.session import engine



app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
app.include_router(api_router, prefix=settings.API_V1_STR)
