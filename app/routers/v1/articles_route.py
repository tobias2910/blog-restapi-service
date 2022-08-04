from typing import List

from fastapi import APIRouter, status

from ... import schemas

TAG_INFORMATION = {
    'name': 'articles',
    'description': 'This endpoint can be used to manage articles'
}

router = APIRouter(
    tags=[TAG_INFORMATION['name']]
)


@router.put(
    '/',
    response_model=List[schemas.ArticleCreated],
    summary='Create a new article',
    description='Creates a new article with the information provided',
    status_code=status.HTTP_201_CREATED,
)
async def add_article(article: List[schemas.Article]):
    return {'successful': True}


@router.get(
    '/',
)
async def get_articles():
    return [{'article': '1'}]


@router.get('/{article_id}')
async def get_article(article_id: str):
    return {'articleID': article_id}


@router.delete('/{article_id}')
async def delete_article(article_id: str):
    return {'articleID': article_id}
