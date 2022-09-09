"""Provides a new router instance, containing all the endpoints available."""
from typing import Dict, List

from fastapi import APIRouter, Depends

from src.routers.v1 import (
    articles_route,
    auth_route,
    projects_route,
    skills_route,
    user_route,
)
from src.util.jwt_authentication import JWTAuthentication

api_router = APIRouter()
api_open_tag_information: List[Dict[str, str]] = []

# Add the routers
api_router.include_router(auth_route.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    articles_route.router,
    prefix="/articles",
    dependencies=[Depends(JWTAuthentication(auto_error=False))],
)
api_router.include_router(
    projects_route.router,
    prefix="/projects",
    dependencies=[Depends(JWTAuthentication(auto_error=False))],
)
api_router.include_router(
    skills_route.router,
    prefix="/skills",
    dependencies=[Depends(JWTAuthentication(auto_error=False))],
)
api_router.include_router(
    user_route.router,
    prefix="/users",
    dependencies=[Depends(JWTAuthentication(auto_error=False))],
)

# Add the open tag information to the array
api_open_tag_information.append(auth_route.TAG_INFORMATION)
api_open_tag_information.append(articles_route.TAG_INFORMATION)
api_open_tag_information.append(projects_route.TAG_INFORMATION)
api_open_tag_information.append(skills_route.TAG_INFORMATION)
api_open_tag_information.append(user_route.TAG_INFORMATION)
