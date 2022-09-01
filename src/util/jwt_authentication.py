from datetime import datetime
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.services.token_service import token_service


class JWTAuthentication(HTTPBearer):
    """
    Provides the logic to validate, whether the client provided
    a valid bearer token within the request.
    """

    def __init__(self, *, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        """
        Checks, whether a valid bearer token was provided in the request
        """
        token: HTTPAuthorizationCredentials = await super().__call__(request)
        if token:
            if not token.scheme == "Bearer":
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN, "Not supported authentication scheme"
                )
            if not self.__verify_token(token.credentials):
                raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid bearer token")
            return token.credentials
        else:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "No credentials provided")

    def __verify_token(self, token: str) -> bool:
        """
        Checks whether the decoded token is valid
        """
        try:
            token_payload = token_service.decode_token(token)
            if datetime.fromtimestamp(token_payload.exp) > datetime.now():
                return True
            else:
                return False
        except BaseException:
            return False
