"""Project services."""
from typing import List, Union

from fastapi import HTTPException, status
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.future import select

from src.models.project_model import Project
from src.schemas.projects_schema import (
    ProjectCreated,
    ProjectDeleted,
    ProjectUpdated,
    UpdateProject,
)


class ProjectsService:
    """Provides all services to manage projects in the database."""

    async def get_project(self, project_id: int, db_session: AsyncSession) -> Union[Project, None]:
        """Get the specified project from the database.

        Args:
            project_id (int): The ID of the project to obtain.
            db_session (AsyncSession): The session for the DB.

        Raises:
            HTTPException: Raised in case an error occurs when obtaining the project information.

        Returns:
            Union[Project, None]: The result of the database. Can be either of type ``Project`` or ``None``,
                in case no projects are stored in the DB.
        """
        try:
            res: AsyncResult = await db_session.execute(select(Project).filter(Project.id == project_id))
            project: Project = res.scalars().first()

            if project is not None:
                return project
            else:
                return None
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining the project",
            ) from BaseException

    async def get_projects(
        self, skip: int, limit: int, db_session: AsyncSession
    ) -> Union[List[Project], None]:
        """Get all projects from the database.

        Args:
            skip: Number of elements to skip from the result set.
            limit: Maximum number of elements to return.
            db_session: The session for the database.

        Returns:
            The result of the database. Can be either of type ``List[Project]`` or ``None``, in
                case no projects are stored in the DB.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when obtaining the projects.

        """
        try:
            res: AsyncResult = await db_session.scalars(select(Project))
            projects_list: List[Project] = res.all()
            if projects_list is not None:
                return projects_list[skip : skip + limit]
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining all projects",
            ) from BaseException

    async def delete_project(self, project_id: int, db_session: AsyncSession) -> ProjectDeleted:
        """Delete the specified project from the database.

        Args:
            project_id (int): The ID of the project to delete from the database.
            db_session (AsyncSession): The session for the database.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when deleting the project.

        Returns:
            ProjectDeleted: The information, whether the specified project was successfully deleted.
        """
        try:
            res: AsyncSession = await db_session.execute(delete(Project).where(Project.id == project_id))
            if res.rowcount != 0:
                await db_session.commit()
                return {"project_id": project_id, "status": "Project deleted"}
            else:
                return {"project_id": project_id, "status": "Project not found"}
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error deleting the project",
            ) from BaseException

    async def create_project(self, project: Project, db_session: AsyncSession) -> ProjectCreated:
        """Insert the provided project in the database.

        Args:
            project (CreateProject): The project object that should be created in the database.
            db_session (AsyncSession): The session for the database.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when creating the project.

        Returns:
            ProjectCreated: The created project including the ID.
        """
        create_project = project.dict()

        try:
            new_project = Project(**create_project)
            db_session.add(new_project)

            await db_session.commit()

            return new_project  # noqa: TC300
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error creating the project",
            ) from BaseException

    async def update_project(
        self, project_id: int, project: UpdateProject, db_session: AsyncSession
    ) -> ProjectUpdated:
        """Update the specified project in the database.

        Args:
            project_id (int): The ID of the project to update.
            project (UpdateProject): The information that shall be updated in the project.
            db_session (AsyncSession):The session for the DB.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when updating the project.

        Returns:
            ProjectUpdated: The status that indicates, whether the update was successful.
        """
        try:
            update_project = project.dict(exclude_unset=True)
            res: AsyncSession = await db_session.execute(
                update(Project)
                .where(Project.id == project_id)
                .values(
                    **update_project,
                )
            )

            if res.rowcount != 0:
                await db_session.commit()
                return {"project_id": project_id, "status": "Project updated"}
            else:
                return {"project_id": project_id, "status": "Project not found"}

        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error updating the project",
            ) from BaseException


projects_service = ProjectsService()
