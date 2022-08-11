from typing import Any, Dict, Optional
from pydantic import BaseSettings, EmailStr, PostgresDsn, validator


class Settings (BaseSettings):
    # API base configuration
    API_PATH: str = '/api/v1'
    API_NAME: str = 'Blog-RestAPI-service'
    API_DESC: str = 'This API can be used to store new articles, posts and skills for the blog frontend'

    # API contact configuration
    API_CONTACT_NAME: str
    API_CONTACT_MAIL: EmailStr
    API_CONTACT_SITE: str

    # Postgres configuration
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PW: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PW'),
            host=values.get('POSTGRES_SERVER'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # JWT Settings
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    # API Admin user configuration
    ADMIN_USER: EmailStr
    ADMIN_PW: str

    class Config(BaseSettings.Config):
        env_file = '.env'
        case_sensitive = True


settings = Settings()
