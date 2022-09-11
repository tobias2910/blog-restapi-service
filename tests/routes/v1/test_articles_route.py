from typing import Dict, List

from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.schemas.articles_schema import ArticleDB
from tests.utils.article import (
    create_article_in_db,
    get_fake_article,
    remove_article_in_db,
)


async def test_create_article(client: AsyncClient, auth_header: Dict[str, str], db_session: AsyncSession):
    # Arrange
    article = get_fake_article()
    # Act
    response = await client.post(f"{settings.API_PATH}/articles/", headers=auth_header, json=article)
    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response["author"] == article["author"]
    assert json_response["tags"] == article["tags"]
    assert json_response["image_url"] == article["image_url"]
    assert json_response["title"] == article["title"]
    assert json_response["description"] == article["description"]
    assert json_response["content"] == article["content"]
    # Cleanup
    await remove_article_in_db(json_response["id"], db_session)


async def test_get_article(
    client: AsyncClient, db_session: AsyncSession, auth_header: Dict[str, str]
) -> None:
    # Arrange
    article = await create_article_in_db(db_session)
    # Act
    response = await client.get(f"{settings.API_PATH}/articles/{article.id}", headers=auth_header)
    json_response = response.json()
    # Assert
    assert json_response["author"] == article.author
    # Cleanup
    await remove_article_in_db(article.id, db_session)


async def test_get_articles(
    client: AsyncClient, db_session: AsyncSession, auth_header: Dict[str, str]
) -> None:
    # Arrange
    article = await create_article_in_db(db_session)
    # Act
    response = await client.get(f"{settings.API_PATH}/articles/", headers=auth_header)
    json_response: List[ArticleDB] = response.json()
    # Assert
    assert isinstance(json_response, List)
    assert next(article_dict for article_dict in json_response if article_dict["id"] == article.id)
    # Cleanup
    await remove_article_in_db(article.id, db_session)


async def test_update_article(
    client: AsyncClient, db_session: AsyncSession, auth_header: Dict[str, str]
) -> None:
    # Arrange
    article = await create_article_in_db(db_session)
    update_article = get_fake_article()
    # Act
    await client.put(
        f"{settings.API_PATH}/articles/{article.id}",
        headers=auth_header,
        json=update_article,
    )
    response = await client.get(f"{settings.API_PATH}/articles/{article.id}", headers=auth_header)
    json_response = response.json()
    # Assert
    assert json_response["author"] == update_article["author"]
    # Cleanup
    await remove_article_in_db(article.id, db_session)


async def test_delete_article(
    client: AsyncClient, db_session: AsyncSession, auth_header: Dict[str, str]
) -> None:
    # Arrange
    article = await create_article_in_db(db_session)
    # Act
    response = await client.delete(f"{settings.API_PATH}/articles/{article.id}", headers=auth_header)
    json_response = response.json()
    # Assert
    assert json_response["article_id"]
    assert json_response["status"] == "Article deleted"
