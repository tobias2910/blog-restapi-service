"""Reads and provides the environment variables as a dict."""
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr, PostgresDsn, validator

# Using this function to avoid issues, that the .env file is
# not being loaded correctly. Further information:
# https://github.com/pydantic/pydantic/issues/1368
load_dotenv()


class Settings(BaseSettings):
    """Reads all the environment variables."""

    # API base configuration
    API_PATH: str = "/api/v1"
    API_NAME: str = "Blog-RestAPI-service"
    API_DESC: str = "This API can be used to store new articles posts and skills for the blog frontend"

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

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Assemble the SQL connection.

        This function is being executed as soon as the class is initialized.

        Args:
            v (Optional[str]): The already assembled value.
            values (Dict[str, Any]): The dictionary containing the
                loaded environment variables.

        Returns:
            str: The assembled PostgreSQL connection.
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(  # type: ignore[no-any-return]
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PW"),
            host=values.get("POSTGRES_SERVER"),
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

    # Sentry settings
    SENTRY_DSN: str

    class Config(BaseSettings.Config):
        """Set the settings."""

        env_file = ".env"  # type: ignore[assignment]
        case_sensitive = True


settings = Settings()
