from typing import List

from src.db.base import get_session
from src.schemas.projects_schema import (
    CreateProject,
    ProjectCreated,
    ProjectDB,
    ProjectDeleted,
    ProjectUpdated,
    UpdateProject,
)
from src.services.projects_service import projects_service
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

TAG_INFORMATION = {
    "name": "projects",
    "description": "This endpoint can be used to manage projects",
}

router = APIRouter(tags=[TAG_INFORMATION["name"]])


@router.get(
    "/{project_id}",
    summary="Get the specified project",
    description="Get the specified project from the database",
    status_code=status.HTTP_200_OK,
    response_model=ProjectDB,
)
async def get_project(
    project_id: int = Path(description="The ID of the project to obtain."),
    db_session: AsyncSession = Depends(get_session),
):
    project = await projects_service.get_project(project_id, db_session)
    return project


@router.get(
    "/",
    summary="Get all articles",
    description="Get all articles stored in the database",
    status_code=status.HTTP_200_OK,
    response_model=List[ProjectDB],
)
async def get_projects(
    db_session: AsyncSession = Depends(get_session),
    skip: int = Query(
        default=0, description="The number of items to skip in the project table"
    ),
    limit: int = Query(
        default=100, description="The maximum number to return from the project table"
    ),
):
    projects = await projects_service.get_projects(skip, limit, db_session)
    return projects


@router.post(
    "/",
    summary="Create a new project",
    description="Creates a new project with the information provided",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectCreated,
)
async def add_project(
    project: CreateProject, db_session: AsyncSession = Depends(get_session)
):
    project = await projects_service.create_project(project, db_session)
    return project


@router.put(
    "/{project_id}",
    summary="Updates an project",
    description="Updated the specified project with the information provided",
    status_code=status.HTTP_200_OK,
    response_model=ProjectUpdated,
)
async def update_project(
    project: UpdateProject,
    project_id: int = Path(description="The ID of the project to update."),
    db_session: AsyncSession = Depends(get_session),
):
    project = await projects_service.update_project(project_id, project, db_session)
    return project


@router.delete(
    "/{project_id}",
    summary="Delete the specified project",
    description="Deletes the specified project in the database",
    status_code=status.HTTP_200_OK,
    response_model=ProjectDeleted,
)
async def delete_project(
    project_id: int = Path(description="The ID of the project to delete."),
    db_session: AsyncSession = Depends(get_session),
):
    response = await projects_service.delete_project(project_id, db_session)
    return response
