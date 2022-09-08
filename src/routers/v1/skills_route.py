"""All skill related endpoints."""
from typing import List, Union

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_session
from src.schemas.skills_schema import SkillAdjusted, SkillDB, SkillSchema, UpdateSkill
from src.services.skills_service import skills_service

TAG_INFORMATION = {
    "name": "skills",
    "description": "This endpoint can be used to manage skills",
}

router = APIRouter(tags=[TAG_INFORMATION["name"]])


@router.get(
    "/{skill_id}",
    summary="Get the specified skill",
    description="Get the specified skill from the database",
    status_code=status.HTTP_200_OK,
    response_model=SkillDB,
)
async def get_skill(
    skill_id: int = Path(description="The ID of the skill to obtain."),
    db_session: AsyncSession = Depends(get_session),
) -> SkillDB:
    """Endpoint for obtaining the specified skill from the database.

    Args:
        skill_id (int): The ID of the skill to obtain.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        SkillDB: The obtained skill or nothing, in case nothing matches the ID.
    """
    skill = await skills_service.get_skill(skill_id, db_session)
    return skill


@router.get(
    "/",
    summary="Get all skills",
    description="Get all skills stored in the database",
    status_code=status.HTTP_200_OK,
    response_model=List[SkillDB],
)
async def get_skills(
    db_session: AsyncSession = Depends(get_session),
    skip: int = Query(default=0, description="The number of items to skip in the skill table"),
    limit: int = Query(default=100, description="The maximum number to return from the skill table"),
) -> Union[List[SkillDB], None]:
    """Endpoint for obtaining all the skills in the database.

    Args:
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.
        skip (int, optional): The number of items to skip. Defaults to 0.
        limit (int, optional): The maximum number of items to return. Defaults to 100.

    Returns:
        List[SkillDB]: The list of skills obtained from the DB.
    """
    skills = await skills_service.get_skills(skip, limit, db_session)
    return skills  # type: ignore[no-any-return]


@router.post(
    "/",
    summary="Create a new skill",
    description="Creates a new skill with the information provided",
    status_code=status.HTTP_201_CREATED,
    response_model=SkillDB,
)
async def add_skill(skill: SkillSchema, db_session: AsyncSession = Depends(get_session)) -> SkillDB:
    """Endpoint to create a new skill in the database.

    Args:
        skill (SkillSchema): The skill to create.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        SkillDB: The information about the created skill.
    """
    skill = await skills_service.create_skill(skill, db_session)
    return skill


@router.put(
    "/{skill_id}",
    summary="Updates an skill",
    description="Updated the specified skills with the information provided",
    status_code=status.HTTP_200_OK,
    response_model=SkillAdjusted,
)
async def update_skill(
    skill: UpdateSkill,
    skill_id: int = Path(description="The ID of the skill to update."),
    db_session: AsyncSession = Depends(get_session),
) -> SkillAdjusted:
    """Endpoint to update an skill in the database.

    Args:
        skill (UpdateSkill): The information to update on the specified skill.
        skill_id (int): The id of the skill to update.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        SkillAdjusted: The status of the update.
    """
    skill = await skills_service.update_skill(skill_id, skill, db_session)
    return skill


@router.delete(
    "/{skill_id}",
    summary="Delete the specified skill",
    description="Deletes the specified skill in the database",
    status_code=status.HTTP_200_OK,
    response_model=SkillAdjusted,
)
async def delete_skill(
    skill_id: int = Path(description="The ID of the skill to delete."),
    db_session: AsyncSession = Depends(get_session),
) -> SkillAdjusted:
    """Endpoint for deleting an skill in the database.

    Args:
        skill_id (int): The skill to delete from the database.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        SkillDeleted: The status indicating the result of the deletion.
    """
    response = await skills_service.delete_skill(skill_id, db_session)
    return response
