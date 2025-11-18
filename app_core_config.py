# =============================================================================
# GoodServices Backend Configuration Management (app/core/config.py)
# =============================================================================
"""
Application configuration management using Pydantic settings.

This module handles all application configuration including:
- Database connection settings
- JWT authentication settings
- API configuration
- File upload settings
- Feature flags
- Logging configuration

Environment variables are loaded from:
1. .env file (project root)
2. System environment variables
3. Default values (if defined)

Usage:
    from app.core.config import settings

    # Access configuration
    db_url = settings.DATABASE_URL
    debug = settings.DEBUG
"""

from typing import List, Optional
from pydantic import Field, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings
import secrets
import os


class Settings(BaseSettings):
    """
    Application settings with validation.

    Reads from environment variables and .env file.
    Validates all settings on application startup.

    Attributes:
        All configuration variables are defined as class attributes
        with Field() for documentation and validation.
    """

    # =========================================================================
    # ENVIRONMENT SETTINGS
    # =========================================================================

    ENVIRONMENT: str = Field(
        default="development",
        env="ENVIRONMENT",
        description="Application environment: development, testing, production"
    )
    DEBUG: bool = Field(
        default=False,
        env="DEBUG",
        description="Enable debug mode (development only!)"
    )
    APP_NAME: str = Field(
        default="GoodServices",
        env="APP_NAME",
        description="Application name for API documentation"
    )
    APP_VERSION: str = Field(
        default="1.0.0",
        description="Application version"
    )

    # =========================================================================
    # DATABASE CONFIGURATION
    # =========================================================================

    MYSQL_HOST: str = Field(
        default="localhost",
        env="MYSQL_HOST",
        description="MySQL server hostname"
    )
    MYSQL_PORT: int = Field(
        default=3306,
        env="MYSQL_PORT",
        description="MySQL server port"
    )
    MYSQL_DATABASE: str = Field(
        default="goodservices",
        env="MYSQL_DATABASE",
        description="MySQL database name"
    )
    MYSQL_USER: str = Field(
        default="goodservices",
        env="MYSQL_USER",
        description="MySQL username"
    )
    MYSQL_PASSWORD: str = Field(
        default="...",
        env="MYSQL_PASSWORD",
        description="MySQL password (required)"
    )
    MYSQL_CHARSET: str = Field(
        default="utf8mb4",
        env="MYSQL_CHARSET",
        description="MySQL character set"
    )
    MYSQL_COLLATION: str = Field(
        default="utf8mb4_unicode_ci",
        env="MYSQL_COLLATION",
        description="MySQL collation"
    )

    # Database pool settings
    DB_POOL_SIZE: int = Field(
        default=5,
        env="DB_POOL_SIZE",
        ge=1,
        le=20,
        description="Database connection pool size"
    )
    DB_MAX_OVERFLOW: int = Field(
        default=10,
        env="DB_MAX_OVERFLOW",
        ge=0,
        le=50,
        description="Maximum overflow connections"
    )
    DB_POOL_TIMEOUT: int = Field(
        default=30,
        env="DB_POOL_TIMEOUT",
        ge=5,
        le=300,
        description="Connection pool timeout in seconds"
    )
    DB_POOL_RECYCLE: int = Field(
        default=3600,
        env="DB_POOL_RECYCLE",
        ge=300,
        description="Connection recycle time in seconds (prevent timeout)"
    )

    # =========================================================================
    # JWT AUTHENTICATION CONFIGURATION
    # =========================================================================

    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        env="SECRET_KEY",
        description="JWT secret key (generate with: secrets.token_urlsafe(32))"
    )
    ALGORITHM: str = Field(
        default="HS256",
        env="ALGORITHM",
        description="JWT algorithm: HS256, HS512, RS256"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
        ge=1,
        le=10080,  # Max 7 days
        description="Access token expiration time in minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        env="REFRESH_TOKEN_EXPIRE_DAYS",
        ge=1,
        le=90,
        description="Refresh token expiration time in days"
    )

    # =========================================================================
    # PASSWORD SECURITY CONFIGURATION
    # =========================================================================

    BCRYPT_ROUNDS: int = Field(
        default=12,
        env="BCRYPT_ROUNDS",
        ge=4,
        le=31,
        description="BCrypt rounds for password hashing (higher = slower)"
    )
    PASSWORD_MIN_LENGTH: int = Field(
        default=6,
        env="PASSWORD_MIN_LENGTH",
        ge=4,
        description="Minimum password length"
    )
    PASSWORD_MIN_DIGITS: int = Field(
        default=2,
        env="PASSWORD_MIN_DIGITS",
        ge=0,
        description="Minimum number of digits in password"
    )
    PASSWORD_REQUIRE_MIXED_CASE: bool = Field(
        default=True,
        env="PASSWORD_REQUIRE_MIXED_CASE",
        description="Require both upper and lowercase letters"
    )

    # =========================================================================
    # CORS CONFIGURATION
    # =========================================================================

    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        env="CORS_ORIGINS",
        description="Comma-separated list of allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True,
        env="CORS_ALLOW_CREDENTIALS",
        description="Allow credentials (cookies, auth headers)"
    )
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        env="CORS_ALLOW_METHODS",
        description="Allowed HTTP methods"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(
        default=["*"],
        env="CORS_ALLOW_HEADERS",
        description="Allowed request headers"
    )

    # =========================================================================
    # API CONFIGURATION
    # =========================================================================

    API_V1_PREFIX: str = Field(
        default="/api/v1",
        env="API_V1_PREFIX",
        description="API v1 prefix path"
    )
    API_TITLE: str = Field(
        default="GoodServices API",
        env="API_TITLE",
        description="API title for documentation"
    )
    API_DESCRIPTION: str = Field(
        default="Community Service Matching Platform API",
        env="API_DESCRIPTION",
        description="API description for documentation"
    )
    API_VERSION: str = Field(
        default="1.0.0",
        env="API_VERSION",
        description="API version for documentation"
    )

    # Request limits
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        env="RATE_LIMIT_PER_MINUTE",
        ge=10,
        le=1000,
        description="API rate limit requests per minute"
    )
    MAX_UPLOAD_SIZE_MB: int = Field(
        default=10,
        env="MAX_UPLOAD_SIZE_MB",
        ge=1,
        le=100,
        description="Maximum upload body size in MB"
    )
    REQUEST_TIMEOUT: int = Field(
        default=30,
        env="REQUEST_TIMEOUT",
        ge=5,
        le=300,
        description="Request timeout in seconds"
    )

    # =========================================================================
    # FILE UPLOAD CONFIGURATION
    # =========================================================================

    UPLOAD_DIR: str = Field(
        default="./uploads",
        env="UPLOAD_DIR",
        description="Directory for uploaded files"
    )
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"],
        env="ALLOWED_EXTENSIONS",
        description="Allowed file extensions"
    )
    MAX_FILE_SIZE_MB: int = Field(
        default=5,
        env="MAX_FILE_SIZE_MB",
        ge=1,
        le=100,
        description="Maximum single file size in MB"
    )
    MAX_FILES_PER_REQUEST: int = Field(
        default=5,
        env="MAX_FILES_PER_REQUEST",
        ge=1,
        le=20,
        description="Maximum files per upload request"
    )

    # =========================================================================
    # LOGGING CONFIGURATION
    # =========================================================================

    LOG_LEVEL: str = Field(
        default="INFO",
        env="LOG_LEVEL",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    LOG_FORMAT: str = Field(
        default="text",
        env="LOG_FORMAT",
        description="Log format: json or text"
    )
    LOG_FILE: Optional[str] = Field(
        default=None,
        env="LOG_FILE",
        description="Log file path (None for stdout only)"
    )
    LOG_SQL_QUERIES: bool = Field(
        default=False,
        env="LOG_SQL_QUERIES",
        description="Log SQL queries (development only!)"
    )

    # =========================================================================
    # FRONTEND CONFIGURATION
    # =========================================================================

    VITE_API_BASE_URL: str = Field(
        default="http://localhost:8000",
        env="VITE_API_BASE_URL",
        description="Frontend API base URL"
    )
    VITE_PORT: int = Field(
        default=5173,
        env="VITE_PORT",
        description="Vite development server port"
    )

    # =========================================================================
    # EMAIL CONFIGURATION (Optional)
    # =========================================================================

    SMTP_HOST: Optional[str] = Field(
        default=None,
        env="SMTP_HOST",
        description="SMTP server hostname"
    )
    SMTP_PORT: Optional[int] = Field(
        default=None,
        env="SMTP_PORT",
        description="SMTP server port"
    )
    SMTP_USER: Optional[str] = Field(
        default=None,
        env="SMTP_USER",
        description="SMTP username"
    )
    SMTP_PASSWORD: Optional[str] = Field(
        default=None,
        env="SMTP_PASSWORD",
        description="SMTP password"
    )
    SMTP_FROM: Optional[str] = Field(
        default=None,
        env="SMTP_FROM",
        description="Default sender email address"
    )
    SMTP_TLS: bool = Field(
        default=True,
        env="SMTP_TLS",
        description="Use TLS for SMTP connection"
    )

    # =========================================================================
    # REDIS CONFIGURATION (Optional)
    # =========================================================================

    REDIS_HOST: str = Field(
        default="localhost",
        env="REDIS_HOST",
        description="Redis server hostname"
    )
    REDIS_PORT: int = Field(
        default=6379,
        env="REDIS_PORT",
        description="Redis server port"
    )
    REDIS_PASSWORD: Optional[str] = Field(
        default=None,
        env="REDIS_PASSWORD",
        description="Redis password"
    )
    REDIS_DB: int = Field(
        default=0,
        env="REDIS_DB",
        description="Redis database number"
    )
    ENABLE_REDIS: bool = Field(
        default=False,
        env="ENABLE_REDIS",
        description="Enable Redis caching"
    )

    # =========================================================================
    # FEATURE FLAGS
    # =========================================================================

    ENABLE_REGISTRATION: bool = Field(
        default=True,
        env="ENABLE_REGISTRATION",
        description="Enable user registration"
    )
    ENABLE_ADMIN_PANEL: bool = Field(
        default=True,
        env="ENABLE_ADMIN_PANEL",
        description="Enable admin panel"
    )
    ENABLE_EMAIL_NOTIFICATIONS: bool = Field(
        default=False,
        env="ENABLE_EMAIL_NOTIFICATIONS",
        description="Enable email notifications"
    )
    ENABLE_STATISTICS: bool = Field(
        default=True,
        env="ENABLE_STATISTICS",
        description="Enable statistics module (REQUIRED)"
    )
    ENABLE_FILE_UPLOAD: bool = Field(
        default=True,
        env="ENABLE_FILE_UPLOAD",
        description="Enable file upload feature"
    )

    # =========================================================================
    # PRODUCTION SETTINGS
    # =========================================================================

    BACKEND_WORKERS: int = Field(
        default=4,
        env="BACKEND_WORKERS",
        ge=1,
        le=16,
        description="Number of backend workers for production"
    )
    FORCE_HTTPS: bool = Field(
        default=False,
        env="FORCE_HTTPS",
        description="Force HTTPS redirect"
    )
    SESSION_COOKIE_SECURE: bool = Field(
        default=False,
        env="SESSION_COOKIE_SECURE",
        description="Secure cookie flag (true for HTTPS)"
    )
    SESSION_COOKIE_SAMESITE: str = Field(
        default="lax",
        env="SESSION_COOKIE_SAMESITE",
        description="Cookie SameSite policy: lax, strict, none"
    )

    # =========================================================================
    # COMPUTED PROPERTIES
    # =========================================================================

    @property
    def DATABASE_URL(self) -> str:
        """
        Construct full database URL from components.

        Format: mysql+pymysql://user:password@host:port/database
        """
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            f"?charset={self.MYSQL_CHARSET}"
        )

    @property
    def REDIS_URL(self) -> str:
        """Construct Redis connection URL."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # =========================================================================
    # VALIDATORS
    # =========================================================================

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @field_validator("CORS_ALLOW_METHODS", mode="before")
    @classmethod
    def parse_cors_methods(cls, v):
        """Parse CORS methods from comma-separated string or list."""
        if isinstance(v, str):
            return [method.strip().upper() for method in v.split(",") if method.strip()]
        return v

    @field_validator("CORS_ALLOW_HEADERS", mode="before")
    @classmethod
    def parse_cors_headers(cls, v):
        """Parse CORS headers from comma-separated string or list."""
        if isinstance(v, str):
            return [header.strip() for header in v.split(",") if header.strip()]
        return v

    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v):
        """Parse allowed extensions from comma-separated string or list."""
        if isinstance(v, str):
            return [ext.strip().lower() for ext in v.split(",") if ext.strip()]
        return v

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v, info):
        """Validate secret key is strong enough for production."""
        environment = info.data.get("ENVIRONMENT", "development")
        if environment == "production":
            if len(v) < 32:
                raise ValueError(
                    "SECRET_KEY must be at least 32 characters in production. "
                    "Generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
            # Check for default values
            if v.startswith("your-") or v == "...":
                raise ValueError(
                    "SECRET_KEY cannot use default or placeholder value in production"
                )
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of: {', '.join(valid_levels)}")
        return v_upper

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v):
        """Validate environment name."""
        valid_envs = ["development", "testing", "production"]
        v_lower = v.lower()
        if v_lower not in valid_envs:
            raise ValueError(f"ENVIRONMENT must be one of: {', '.join(valid_envs)}")
        return v_lower

    @field_validator("DEBUG")
    @classmethod
    def validate_debug_mode(cls, v, info):
        """Warn if DEBUG is enabled in production."""
        environment = info.data.get("ENVIRONMENT", "development")
        if environment == "production" and v:
            raise ValueError(
                "DEBUG mode must be disabled in production for security!"
            )
        return v

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v):
        """Validate JWT algorithm."""
        valid_algorithms = ["HS256", "HS512", "RS256", "RS512"]
        if v not in valid_algorithms:
            raise ValueError(f"ALGORITHM must be one of: {', '.join(valid_algorithms)}")
        return v

    @field_validator("SESSION_COOKIE_SAMESITE")
    @classmethod
    def validate_cookie_samesite(cls, v):
        """Validate SameSite policy."""
        valid_policies = ["lax", "strict", "none"]
        if v.lower() not in valid_policies:
            raise ValueError(f"SESSION_COOKIE_SAMESITE must be one of: {', '.join(valid_policies)}")
        return v.lower()

    # =========================================================================
    # PYDANTIC CONFIGURATION
    # =========================================================================

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Create global settings instance (singleton pattern)
settings = Settings()

# =============================================================================
# VALIDATION ON STARTUP
# =============================================================================

def validate_settings() -> None:
    """
    Validate all settings on application startup.

    This function is called in app/main.py to ensure all
    configuration is valid before the application starts.

    Raises:
        ValueError: If any validation fails
    """
    # Basic validation
    if not settings.MYSQL_PASSWORD or settings.MYSQL_PASSWORD == "...":
        raise ValueError("MYSQL_PASSWORD is required and cannot be empty")

    # Verify upload directory exists or can be created
    import os
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Log configuration summary
    from app.core.logging import logger
    logger.info(f"Application started in {settings.ENVIRONMENT} mode")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
    logger.info(f"CORS origins: {', '.join(settings.CORS_ORIGINS)}")
    logger.info(f"Statistics enabled: {settings.ENABLE_STATISTICS}")


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["settings", "Settings", "validate_settings"]
