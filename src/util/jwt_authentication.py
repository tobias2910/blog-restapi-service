"""Functions for handling JWT authentication."""
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.services.token_service import token_service


class JWTAuthentication(HTTPBearer):
    """Provides the logic to extract and validate a JWT token."""

    def __init__(self, *, auto_error: bool = True):
        """Initiate an new instance.

        Args:
            auto_error (bool, optional): Flag that indicates, whether to throw an error, in
                case no token was provided. Defaults to ```True```.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """Validate the credentials in the request.

        Checks, whether a valid bearer token was provided in the request.

        Args:
            request (Request): The current request object, containing all client related information.

        Raises:
            HTTPException: No token of scheme type "Bearer" provided.
            HTTPException: Not a valid bearer token provided.
            HTTPException: No credentials provided.

        Returns:
            HTTPAuthorizationCredentials: The validated and valid token.
        """
        token: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)

        if token:
            if token.scheme != "Bearer":
                raise HTTPException(status.HTTP_403_FORBIDDEN, "Not supported authentication scheme")
            if not self.__verify_token(token.credentials):
                raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid bearer token")
            return token
        else:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "No credentials provided")

    def __verify_token(self, token: str) -> bool:
        """Verify the provided token.

        Verifies the token and checks, whether the decoded token
            is still valid.

        Args:
            token (str): The token that should be validated.

        Returns:
            bool: The result, whether the provided token is valid.
        """
        try:
            token_payload = token_service.decode_token(token)
            if datetime.fromtimestamp(token_payload.exp) > datetime.now():
                return True
            else:
                return False
        except BaseException:
            return False
