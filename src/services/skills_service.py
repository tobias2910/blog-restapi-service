"""Skills service."""
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.future import select

from src.models.skill_model import Skill
from src.schemas.skills_schema import SkillAdjusted, SkillDB, SkillSchema


class SkillsService:
    """Provides all services to manage skills in the database."""

    async def get_skill(self, skill_id: int, db_session: AsyncSession) -> SkillDB:
        """Get the specified skill from the database.

        Args:
            skill_id: The ID of the skill to obtain from the database.
            db_session: The session for the database.

        Returns:
            SkillDB: The result of the database. Can be either of type ```SkillDB``` or ```None```, in
                case no row matches the provided ID.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when obtaining the skill.
        """
        try:
            res: AsyncResult = await db_session.execute(select(Skill).filter(Skill.id == skill_id))
            skill: SkillDB = res.scalars().first()

            if skill is not None:
                return skill
            else:
                return None
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining the skill",
            ) from BaseException

    async def get_skills(self, skip: int, limit: int, db_session: AsyncSession) -> List[Skill]:
        """Get all skills from the database.

        Args:
            skip: Number of elements to skip from the result set.
            limit: Maximum number of elements to return.
            db_session: The session for the database.

        Returns:
            List[Skill]: The result of the database.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when obtaining the skills.

        """
        try:
            res: AsyncResult = await db_session.scalars(select(Skill))
            skill_list: List[Skill] = res.all()
            if skill_list is not None:
                return skill_list[skip : skip + limit]
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining all skills",
            ) from BaseException

    async def delete_skill(self, skill_id: int, db_session: AsyncSession) -> SkillAdjusted:
        """Delete the specified skill from the database.

        Args:
            skill_id (int): The ID of the skill to delete from the database.
            db_session (AsyncSession): The session for the database.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when deleting the skill.

        Returns:
            SkillDeleted: The information, whether the specified skill was successfully deleted.
        """
        try:
            res: AsyncSession = await db_session.execute(delete(Skill).where(Skill.id == skill_id))
            if res.rowcount != 0:
                await db_session.commit()
                return {"skill_id": skill_id, "status": "Skill deleted"}
            else:
                return {"skill_id": skill_id, "status": "Skill not found"}
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error deleting the skill",
            ) from BaseException

    async def create_skill(self, skill: SkillSchema, db_session: AsyncSession) -> SkillDB:
        """Insert the provided skill in the database.

        Args:
            skill (SkillSchema): The skill object that should be created in the database.
            db_session (AsyncSession): The session for the database.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when creating the skill.

        Returns:
            SkillCreated: The created skill including the ID.
        """
        try:
            create_skill = skill.dict()
            new_skill = Skill(
                **create_skill,
            )
            db_session.add(new_skill)

            await db_session.commit()

            return new_skill  # noqa: TC300
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error creating the skill",
            ) from BaseException

    async def update_skill(
        self, skill_id: int, skill: SkillSchema, db_session: AsyncSession
    ) -> SkillAdjusted:
        """Update the specified skill in the database.

        Args:
            skill_id (int): The ID of the skill to update.
            skill (SkillSchema): The information that shall be updated in the skill.
            db_session (AsyncSession):The session for the DB.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when updating the skill.

        Returns:
            SkillUpdated: The status that indicates, whether the update was successful.
        """
        try:
            update_skill = skill.dict(exclude_unset=True)
            res: AsyncSession = await db_session.execute(
                update(Skill)
                .where(Skill.id == skill_id)
                .values(
                    **update_skill,
                )
            )

            if res.rowcount != 0:
                await db_session.commit()
                return SkillAdjusted(skill_id=skill_id, status="Skill updated")
            else:
                return SkillAdjusted(skill_id=skill_id, status="Skill not found")

        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error updating the skill",
            ) from BaseException


skills_service = SkillsService()
