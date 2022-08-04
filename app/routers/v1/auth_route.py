from fastapi import APIRouter, status

TAG_INFORMATION = {
    'name': 'auth',
    'description': 'This endpoint can be used to perform the authentication'
}

router = APIRouter(
    tags=[TAG_INFORMATION['name']]
)


@router.get(
    '/',
    summary='Conduct the authentication',
    description='Creates a new article with the information provided',
    status_code=status.HTTP_200_OK
)
async def authenticate_user():
    return
