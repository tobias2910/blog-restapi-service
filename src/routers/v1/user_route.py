from src.db.base import get_session
from src.schemas.user_schema import CreateUser, UserCreated, UserDeleted, UserSchema
from src.services.user_service import user_service
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

TAG_INFORMATION = {
    "name": "users",
    "description": "This endpoint is for managing users of the API",
}

router = APIRouter(tags=[TAG_INFORMATION["name"]])


@router.post(
    "/",
    summary="Create a new user",
    description="Create a new user in the the database to grant access to the API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreated,
)
async def create_user(
    user_information: CreateUser,
    db_session: AsyncSession = Depends(get_session),
):
    user = await user_service.create_new_user(
        db_session, user_information.email, user_information.password
    )
    return user


@router.delete(
    "/",
    summary="Deletes a user",
    description="Deletes the specified user from the database",
    status_code=status.HTTP_200_OK,
    response_model=UserDeleted,
)
async def delete_user(
    user_information: UserSchema,
    db_session: AsyncSession = Depends(get_session),
):
    user = await user_service.delete_user(db_session, user_information.email)
    return user
