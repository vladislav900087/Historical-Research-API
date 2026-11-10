from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = 'Historical Research API'
    SECRET_KEY: str = 'supersecretkeyinproduction'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
