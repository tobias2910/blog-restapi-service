from typing import List, Dict
from fastapi import APIRouter, Depends

from app.util.jwt_authentication import JWT_Authentication
from app.routers.v1 import articles_route, auth_route, projects_route, user_route

api_router = APIRouter()
api_open_tag_information: List[Dict[str, str]] = []

# Add the routers
api_router.include_router(auth_route.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    articles_route.router,
    prefix="/articles",
    dependencies=[Depends(JWT_Authentication(auto_error=False))],
)
api_router.include_router(
    projects_route.router,
    prefix="/projects",
    dependencies=[Depends(JWT_Authentication(auto_error=False))],
)
api_router.include_router(
    user_route.router,
    prefix="/users",
    dependencies=[Depends(JWT_Authentication(auto_error=False))],
)

# Add the open tag information to the array
api_open_tag_information.append(auth_route.TAG_INFORMATION)
api_open_tag_information.append(articles_route.TAG_INFORMATION)
api_open_tag_information.append(projects_route.TAG_INFORMATION)
api_open_tag_information.append(user_route.TAG_INFORMATION)
