from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import async_session
from app.services.user_service import user_service
from app.services.token_service import token_service

from app.schemas.token_schema import Auth_Token


class Auth_service():
    '''
    Provides services for the authentication against the API
    '''
    async def authenticate_user(self, mail: str, password: str) -> Auth_Token:
        '''
        Conducts the authentication and provide the access tokens, in case the mail
        and password is correct.
        '''
        async with async_session() as session:
            session: Session
            async with session.begin():
                user = await user_service.get_user(session, mail)
                if user is None or not user.verify_password(password):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Invalid email and / or password',
                    )

                access_tokens = token_service.generate_auth_tokens(
                    str(user.email))

                return access_tokens


auth_service = Auth_service()
