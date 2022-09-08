"""All article related endpoints."""
from typing import List, Union

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_session
from src.schemas.articles_schema import (
    ArticleCreated,
    ArticleDB,
    ArticleDeleted,
    ArticleUpdated,
    CreateArticle,
    UpdateArticle,
)
from src.services.articles_service import articles_service

TAG_INFORMATION = {
    "name": "articles",
    "description": "This endpoint can be used to manage articles",
}

router = APIRouter(tags=[TAG_INFORMATION["name"]])


@router.get(
    "/{article_id}",
    summary="Get the specified article",
    description="Get the specified article from the database",
    status_code=status.HTTP_200_OK,
    response_model=ArticleDB,
)
async def get_article(
    article_id: int = Path(description="The ID of the article to obtain."),
    db_session: AsyncSession = Depends(get_session),
) -> ArticleDB:
    """Endpoint for obtaining the specified article from the database.

    Args:
        article_id (int, optional): The ID of the article to obtain.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        ArticleDB: The obtained article or nothing, in case nothing matches the ID.
    """
    article = await articles_service.get_article(article_id, db_session)
    return article


@router.get(
    "/",
    summary="Get all articles",
    description="Get all articles stored in the database",
    status_code=status.HTTP_200_OK,
    response_model=List[ArticleDB],
)
async def get_articles(
    db_session: AsyncSession = Depends(get_session),
    skip: int = Query(default=0, description="The number of items to skip in the article table"),
    limit: int = Query(default=100, description="The maximum number to return from the article table"),
) -> Union[List[ArticleDB], None]:
    """Endpoint for obtaining all the articles in the database.

    Args:
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.
        skip (int, optional): The number of items to skip. Defaults to 0.
        limit (int, optional): The maximum number of items to return. Defaults to 100.

    Returns:
        List[ArticleDB]: The list of articles obtained from the DB.
    """
    articles = await articles_service.get_articles(skip, limit, db_session)
    return articles  # type: ignore[no-any-return]


@router.post(
    "/",
    summary="Create a new article",
    description="Creates a new article with the information provided",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleCreated,
)
async def add_article(
    article: CreateArticle, db_session: AsyncSession = Depends(get_session)
) -> ArticleCreated:
    """Endpoint to create a new article in the database.

    Args:
        article (CreateArticle): The article to create.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        Union[ArticleCreated, None]: The information about the created article.
    """
    article = await articles_service.create_article(article, db_session)
    return article


@router.put(
    "/{article_id}",
    summary="Updates an article",
    description="Updated the specified article with the information provided",
    status_code=status.HTTP_200_OK,
    response_model=ArticleUpdated,
)
async def update_article(
    article: UpdateArticle,
    article_id: int = Path(description="The ID of the article to update."),
    db_session: AsyncSession = Depends(get_session),
) -> UpdateArticle:
    """Endpoint to update an article in the database.

    Args:
        article (UpdateArticle): The information to update on the specified article.
        article_id (int): The id of the article to update.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        UpdateArticle: The status of the update.
    """
    article = await articles_service.update_article(article_id, article, db_session)
    return article


@router.delete(
    "/{article_id}",
    summary="Delete the specified article",
    description="Deletes the specified article in the database",
    status_code=status.HTTP_200_OK,
    response_model=ArticleDeleted,
)
async def delete_article(
    article_id: int = Path(description="The ID of the article to delete."),
    db_session: AsyncSession = Depends(get_session),
) -> ArticleDeleted:
    """Endpoint for deleting an article in the database.

    Args:
        article_id (int): The article to delete from the database.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        ArticleDeleted: The status indicating the result of the deletion.
    """
    response = await articles_service.delete_article(article_id, db_session)
    return response
