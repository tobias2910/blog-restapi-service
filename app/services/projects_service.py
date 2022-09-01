from typing import List, Union
from fastapi import HTTPException, status

from sqlalchemy import delete, update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from app.models.project_model import Project
from app.schemas.projects_schema import ProjectCreated, CreateProject, ProjectUpdated


class Projects_service:
    """
    Provides all services to manage projects in the database
    """

    async def get_project(
        self, project_id: int, db_session: AsyncSession
    ) -> Union[Project, None]:
        """
        Gets the specified project from the database.
        """
        try:
            res: AsyncResult = await db_session.execute(
                select(Project).filter(Project.id == project_id)
            )
            project: Project = res.scalars().first()

            if project is not None:
                return project
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining the project",
            )

    async def get_projects(
        self, skip: int, limit: int, db_session: AsyncSession
    ) -> Union[List[Project], None]:
        """
        Gets all projects from the database.
        """
        try:
            res: AsyncResult = await db_session.scalars(select(Project))
            projects_list: List[Project] = res.all()
            if projects_list is not None:
                return projects_list[skip : skip + limit]
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining all projects",
            )

    async def delete_project(self, project_id: int, db_session: AsyncSession):
        """
        Deletes the specified project from the database.
        """
        try:
            res: AsyncSession = await db_session.execute(
                delete(Project).where(Project.id == project_id)
            )
            if res.rowcount != 0:
                await db_session.commit()
                return {"project_id": project_id, "status": "Project deleted"}
            return {"project_id": project_id, "status": "Project not found"}
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error deleting the project",
            )

    async def create_project(
        self, project: CreateProject, db_session: AsyncSession
    ) -> ProjectCreated:
        """
        Inserts the provided project in the database.
        """
        create_project = project.dict(exclude={"tags"})
        try:
            new_project = Project(
                **create_project,
                tags=";".join(project.tags),
            )
            db_session.add(new_project)

            await db_session.commit()
            # Split the tags string again, since it was only required for the DB
            new_project.tags = new_project.tags.split(";")

            return new_project
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error creating the project",
            )

    async def update_project(
        self, project_id: int, project: CreateProject, db_session: AsyncSession
    ) -> ProjectUpdated:
        """
        Updates the specified project in the database.
        """
        try:
            update_project = project.dict(exclude_unset=True)
            update_project["tags"] = ";".join(project.tags)
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
            return {"project_id": project_id, "status": "Project not found"}

        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error updating the project",
            )


projects_service = Projects_service()
