from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra = 'ignore')

    user_database_uri: str
    mail_port: int
    user_uri: str
    jwt_key: str
    jwt_algo: str
    super_key: str
    book_database_uri: str

    
settings = Settings()