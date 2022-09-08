"""User model for the database."""
import hmac

import bcrypt
from sqlalchemy import Column, Integer, String

from src.db.base import Base


class User(Base):
    """Represents the user table in the database."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String)

    @property
    def hash_password(self) -> None:
        """Init the property.

        Raises:
            AttributeError: Raised, in case no password provided.
        """
        raise AttributeError("Missing_password")

    @hash_password.setter
    def hash_password(self, hash_password: str) -> None:
        """Hash the password.

        The setter function for the ```property```. Ensures, that the
        password is hashed before being assigned to the property.

        Args:
            hash_password (str): The password to hash.
        """
        self.password = bcrypt.hashpw(hash_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        """Verify the password.

        Verifies, whether the provided password matches the password
        stored for the current user.

        Args:
            password (str): The password to verify.

        Returns:
            bool: The flag indicating, whether the password is valid.
        """
        self_encoded_password: bytes = self.password.encode("utf-8")
        self_password_hash: bytes = bcrypt.hashpw(password.encode("utf-8"), self_encoded_password)
        return hmac.compare_digest(self_encoded_password, self_password_hash)
