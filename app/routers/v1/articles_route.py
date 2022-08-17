from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_session
from app.services.articles_service import articles_service
from app.schemas.articles_schema import Article, ArticleCreated, ArticleUpdate


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
)
async def get_article(article_id: int, db_session: AsyncSession = Depends(get_session)):
    article = await articles_service.get_article(article_id, db_session)
    return article


@router.get(
    "/",
    summary="Get all articles",
    description="Get all articles stored in the database",
    status_code=status.HTTP_200_OK,
)
async def get_articles(db_session: AsyncSession = Depends(get_session)):
    articles = await articles_service.get_articles(db_session)
    return articles


@router.post(
    "/",
    response_model=ArticleCreated,
    summary="Create a new article",
    description="Creates a new article with the information provided",
    status_code=status.HTTP_201_CREATED,
)
async def add_article(
    article: Article, db_session: AsyncSession = Depends(get_session)
):
    article = await articles_service.create_article(article, db_session)
    return article


@router.put(
    "/{article_id}",
    summary="Updates an article",
    description="Updated the specified article with the information provided",
    status_code=status.HTTP_200_OK,
)
async def update_article(
    article_id: int,
    article: ArticleUpdate,
    db_session: AsyncSession = Depends(get_session),
):
    article = await articles_service.update_article(article_id, article, db_session)
    return article


@router.delete(
    "/{article_id}",
    summary="Delete the specified article",
    description="Deletes the specified article in the database",
    status_code=status.HTTP_200_OK,
)
async def delete_article(
    article_id: int, db_session: AsyncSession = Depends(get_session)
):
    response = await articles_service.delete_article(article_id, db_session)
    return response
