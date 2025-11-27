from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: str = "image/jpeg,image/png,image/gif,audio/ogg,audio/webm,application/pdf"
    
    class Config:
        env_file = ".env"
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        return self.ALLOWED_FILE_TYPES.split(",")


settings = Settings()
