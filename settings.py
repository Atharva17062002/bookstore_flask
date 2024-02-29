from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra = 'ignore')

    database_uri: str
    mail_port: int
    user_uri: str
    jwt_key: str
    jwt_algo: str
    super_user_secret_key: str

    
settings = Settings()