from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    name: str

    @computed_field
    @property
    def url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.name,
        ).render_as_string(hide_password=False)


class YandexGPTSettings(BaseModel):
    APi_URL: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    API_KEY: str
    FOLDER_ID: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="_")

    SERVICE_PORT: int = 8000
    database: DatabaseSettings
    yandex_gpt: YandexGPTSettings

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
