import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from .routers.api import api_router, api_open_tag_information
from .config.settings import settings


# Init the app
app = FastAPI(
    title=settings.API_NAME,
    description=settings.API_DESC,
    contact={
        'name': settings.API_CONTACT_NAME,
        'url': settings.API_CONTACT_SITE,
        'email': settings.API_CONTACT_MAIL,
    },
    openapi_url=f"{settings.API_PATH}/openapi.json",
    openapi_tags=api_open_tag_information
)

# Add the middlewares to the chain
app.add_middleware(CORSMiddleware)
app.add_middleware(GZipMiddleware)


# Attach all the routers
app.include_router(api_router, prefix=settings.API_PATH)


@app.on_event('startup')  # type: ignore
async def establish_connection():
    pass


@app.on_event('shutdown')  # type: ignore
async def close_connection():
    pass

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)  # type: ignore
