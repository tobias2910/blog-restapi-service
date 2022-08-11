from typing import List, Dict
from fastapi import APIRouter, Depends

from app.config.jwt_authentication import JWT_Authentication
from app.routers.v1 import articles_route, auth_route

api_router = APIRouter()
api_open_tag_information: List[Dict[str, str]] = []

# Add the routers
api_router.include_router(
    articles_route.router, prefix='/articles', tags=['articles'],
    dependencies=[Depends(JWT_Authentication(auto_error=False))]
)
api_router.include_router(
    auth_route.router, prefix='/auth', tags=['auth'])

# Add the open tag information to the array
api_open_tag_information.append(
    articles_route.TAG_INFORMATION)
api_open_tag_information.append(
    auth_route.TAG_INFORMATION)
