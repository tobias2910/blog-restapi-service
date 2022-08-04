from sqlalchemy.future import select
from sqlalchemy.orm import Session

from user_service import User_service
from models.user_model import User


class Auth_service():
    '''
    '''

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def authenticate_user(self, mail: str, password: str) -> bool:

        user: User = await
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return user
