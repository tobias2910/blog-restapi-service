from typing import List, Dict
from fastapi import APIRouter

from .v1 import articles

api_router = APIRouter()
api_open_tag_information: List[Dict[str, str]] = []

# Add the routers
api_router.include_router(
    articles.router, prefix='/articles', tags=['articles'])

# Add the open tag information to the array
api_open_tag_information.append(articles.TAG_INFORMATION)
