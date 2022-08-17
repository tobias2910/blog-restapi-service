import bcrypt
import hmac
from sqlalchemy import Column, Integer, String

from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String)

    @property
    def hash_password(self):
        raise AttributeError("Password not readable")

    @hash_password.setter
    def hash_password(self, hash_password: str):
        """
        Hash the provided password and store in the password field
        """
        self.password = bcrypt.hashpw(hash_password, bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        """
        Check, whether the passed password equals the one that is stored
        for the current user.
        """
        self_encoded_password: str = self.password.encode("utf-8")
        self_password_hash: str = bcrypt.hashpw(
            password.encode("utf-8"), self_encoded_password
        )
        return hmac.compare_digest(self_encoded_password, self_password_hash)
