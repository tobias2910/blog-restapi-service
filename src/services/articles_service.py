"""Articles service."""
from datetime import datetime
from typing import List, Union

from fastapi import HTTPException, status
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.future import select

from src.models.article_model import Article
from src.schemas.articles_schema import (
    ArticleCreated,
    ArticleDB,
    ArticleDeleted,
    ArticleUpdated,
    CreateArticle,
    UpdateArticle,
)


class ArticlesService:
    """Provides all services to manage articles in the database."""

    async def get_article(self, article_id: int, db_session: AsyncSession) -> Union[ArticleDB, None]:
        """Get the specified article from the database.

        Args:
            article_id: The ID of the article to obtain from the database.
            db_session: The session for the database.

        Returns:
            The result of the database. Can be either of type ``ArticleDB`` or ``None``, in
                case no row matches the provided ID.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when obtaining the article.
        """
        try:
            res: AsyncResult = await db_session.execute(select(Article).filter(Article.id == article_id))
            article: ArticleDB = res.scalars().first()

            if article is not None:
                return article
            else:
                return None
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining the article",
            ) from BaseException

    async def get_articles(
        self, skip: int, limit: int, db_session: AsyncSession
    ) -> Union[List[Article], None]:
        """Get all articles from the database.

        Args:
            skip: Number of elements to skip from the result set.
            limit: Maximum number of elements to return.
            db_session: The session for the database.

        Returns:
            The result of the database. Can be either of type ``List[Article]`` or ``None``, in
                case no articles are stored in the DB.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when obtaining the articles.

        """
        try:
            res: AsyncResult = await db_session.scalars(select(Article))
            articles_list: List[Article] = res.all()
            if articles_list is not None:
                return articles_list[skip : skip + limit]
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining all articles",
            ) from BaseException

    async def delete_article(self, article_id: int, db_session: AsyncSession) -> ArticleDeleted:
        """Delete the specified article from the database.

        Args:
            article_id (int): The ID of the article to delete from the database.
            db_session (AsyncSession): The session for the database.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when deleting the article.

        Returns:
            ArticleDeleted: The information, whether the specified article was successfully deleted.
        """
        try:
            res: AsyncSession = await db_session.execute(delete(Article).where(Article.id == article_id))
            if res.rowcount != 0:
                await db_session.commit()
                return {"article_id": article_id, "status": "Article deleted"}
            else:
                return {"article_id": article_id, "status": "Article not found"}
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error deleting the article",
            ) from BaseException

    async def create_article(self, article: CreateArticle, db_session: AsyncSession) -> ArticleCreated:
        """Insert the provided article in the database.

        Args:
            article (CreateArticle): The article object that should be created in the database.
            db_session (AsyncSession): The session for the database.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when creating the article.

        Returns:
            ArticleCreated: The created article including the ID.
        """
        create_article = article.dict(exclude={"tags"})
        try:
            new_article = Article(
                **create_article,
                tags=";".join(article.tags),
                created_at=datetime.now(),
            )
            db_session.add(new_article)

            await db_session.commit()
            new_article.tags = new_article.tags.split(";")

            return new_article  # noqa: TC300
        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error creating the article",
            ) from BaseException

    async def update_article(
        self, article_id: int, article: UpdateArticle, db_session: AsyncSession
    ) -> ArticleUpdated:
        """Update the specified article in the database.

        Args:
            article_id (int): The ID of the article to update.
            article (UpdateArticle): The information that shall be updated in the article.
            db_session (AsyncSession):The session for the DB.

        Raises:
            HTTPException: Is being thrown as soon as an error occurs when updating the article.

        Returns:
            ArticleUpdated: The status that indicates, whether the update was successful.
        """
        try:
            update_article = article.dict(exclude_unset=True)
            update_article["tags"] = ";".join(article.tags)
            res: AsyncSession = await db_session.execute(
                update(Article)
                .where(Article.id == article_id)
                .values(
                    **update_article,
                    updated_at=datetime.now(),
                )
            )

            if res.rowcount != 0:
                await db_session.commit()
                return ArticleUpdated(article_id=article_id, status="Article updated")
            else:
                return ArticleUpdated(article_id=article_id, status="Article not found")

        except BaseException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error updating the article",
            ) from BaseException


articles_service = ArticlesService()
