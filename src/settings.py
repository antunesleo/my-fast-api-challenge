from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_host: str
    mongo_port: int
    mongo_username: str
    mongo_password: str

    global_api_key: str

    is_test: bool = False


settings = Settings()
