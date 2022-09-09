"""Initializes the App with the provided configurations and middlewares."""
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.config.settings import settings
from src.routers.api import api_open_tag_information, api_router

# Init the Sentry client
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
)

# Init the app
app = FastAPI(
    title=settings.API_NAME,
    description=settings.API_DESC,
    contact={
        "name": settings.API_CONTACT_NAME,
        "url": settings.API_CONTACT_SITE,
        "email": settings.API_CONTACT_MAIL,
    },
    openapi_url=f"{settings.API_PATH}/openapi.json",
    openapi_tags=api_open_tag_information,
    docs_url="/api/swagger",
)

# Add the middlewares to the chain
# TODO: Configure CORS correctly
app.add_middleware(CORSMiddleware)
app.add_middleware(GZipMiddleware)


# Attach all the routers
app.include_router(api_router, prefix=settings.API_PATH)
