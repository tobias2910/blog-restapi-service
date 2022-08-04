from typing import List, Dict
from fastapi import APIRouter, Depends

from ..config.authentication import HTTP_authentication
from .v1 import articles_route, auth_route

api_router = APIRouter()
api_open_tag_information: List[Dict[str, str]] = []

# Add the routers
api_router.include_router(
    articles_route.router, Depends(HTTP_authentication), prefix='/articles', tags=['articles'])

# Add the open tag information to the array
api_open_tag_information.append(articles.TAG_INFORMATION)
