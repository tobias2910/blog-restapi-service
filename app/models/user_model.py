from sqlalchemy import Column, Integer, String, func

from db.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String)

    @property
    def hash_password(self):
        raise AttributeError('Password not readable')

    @hash_password.setter
    def hash_password(self, hash_password: str):
        self.password = func.crypt(hash_password, func.gen_salt('md5'))

    def verify_password(self, hash_password: str):
        pw_hash = func.crypt(self.password, hash_password)
        return self.password == pw_hash
