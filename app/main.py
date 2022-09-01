from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.routers.api import api_router, api_open_tag_information
from app.config.settings import settings

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
    docs_url=f"/api/swagger",
)

# Add the middlewares to the chain
app.add_middleware(CORSMiddleware)
app.add_middleware(GZipMiddleware)


# Attach all the routers
app.include_router(api_router, prefix=settings.API_PATH)
