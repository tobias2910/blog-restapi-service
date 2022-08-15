from typing import List, Union
from datetime import datetime
from fastapi import HTTPException, status

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from app.models.article_model import Article
from app.schemas.articles_schema import Article as Article_schema


class Articles_service:
    """
    Provides all services to manage articles in the database
    """

    async def get_article(
        self, article_id: int, db_session: AsyncSession
    ) -> Union[Article_schema, None]:
        """
        Gets the specified article from the database.
        """
        try:
            res: AsyncResult = await db_session.execute(
                select(Article).filter(Article.id == article_id)
            )
            article: Article_schema = res.scalars().first()

            if article is not None:
                return Article_schema(article)
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining the article",
            )

    async def get_articles(
        self, db_session: AsyncSession
    ) -> Union[List[Article_schema], None]:
        """
        Gets all articles from the database.
        """
        try:
            res: AsyncResult = await db_session.scalars(select(Article))
            articles_list: List[Article_schema] = res.all()
            if articles_list is not None:
                return articles_list
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error obtaining all articles",
            )

    async def delete_article(self, article_id: int, db_session: AsyncSession):
        """
        Deletes the specified article from the database.
        """
        try:
            res: AsyncSession = await db_session.execute(
                delete(Article).where(Article.id == article_id)
            )
            if res.rowcount != 0:
                await db_session.commit()
                return {"articleID": article_id, "status": "Article deleted"}
            return {"articleID": article_id, "status": "Article not found"}
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error deleting the article",
            )

    async def create_article(
        self, article: Article_schema, db_session: AsyncSession
    ) -> Article_schema:
        """
        Inserts the provided article in the database.
        """
        try:
            new_article = Article(
                title=article.title,
                author=article.author,
                image_url=article.imageUrl,
                description=article.summary,
                content=article.content,
                tags=";".join(article.tags),
                created_at=datetime.now(),
            )
            db_session.add(new_article)

            await db_session.commit()

            return new_article
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Error creating the article",
            )


articles_service = Articles_service()
