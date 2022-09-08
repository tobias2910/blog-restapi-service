from typing import Any, Dict

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.articles_schema import CreateArticle
from src.services.articles_service import articles_service


def get_fake_article() -> Dict[str, Any]:
    fake = Faker()

    article = {
        "author": fake.name(),
        "tags": [fake.unique.company_suffix() for _ in range(3)],
        "image_url": fake.domain_name(),
        "title": fake.sentence(nb_words=3),
        "description": fake.sentence(nb_words=14),
        "content": fake.paragraph(nb_sentences=5),
    }

    return article


async def create_article_in_db(db_session: AsyncSession):
    article = CreateArticle(**get_fake_article())
    response = await articles_service.create_article(article, db_session)
    return response


async def remove_article_in_db(article_id: int, db_session: AsyncSession):
    await articles_service.delete_article(article_id, db_session)
