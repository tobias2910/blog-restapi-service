"""All projects related endpoints."""
from typing import List

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

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
) -> ProjectDB:
    """Endpoint for obtaining the specified project from the database.

    Args:
        project_id (int, optional): The ID of the project to obtain.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        ProjectDB: The obtained project or nothing, in case nothing matches the ID.
    """
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
    skip: int = Query(default=0, description="The number of items to skip in the project table"),
    limit: int = Query(default=100, description="The maximum number to return from the project table"),
) -> List[ProjectDB]:
    """Endpoint to obtain all projects in the database.

    Args:
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.
        skip (int, optional): The number of items to skip. Defaults to 0.
        limit (int, optional): The maximum number of items to return. Defaults to 100.

    Returns:
        List[ProjectDB]: The list of articles obtained from the DB.
    """
    projects = await projects_service.get_projects(skip, limit, db_session)
    return projects  # type: ignore[no-any-return]


@router.post(
    "/",
    summary="Create a new project",
    description="Creates a new project with the information provided",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectCreated,
)
async def add_project(
    project: CreateProject, db_session: AsyncSession = Depends(get_session)
) -> ProjectCreated:
    """Endpoint to create a new project in the database.

    Args:
        project (CreateProject): The project to create.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        ProjectCreated: The information about the created project.
    """
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
) -> ProjectUpdated:
    """Endpoint to update a project in the database.

    Args:
        project (UpdateProject): The information to update on the specified project.
        project_id (int): The id of the project to update.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        UpdateProject: The status of the update.
    """
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
) -> ProjectDeleted:
    """Endpoint for deleting a project in the database.

    Args:
        project_id (int): The project to delete from the database.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        ProjectDeleted: The status indicating the result of the deletion.
    """
    response = await projects_service.delete_project(project_id, db_session)
    return response
