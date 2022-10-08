from pydantic import BaseSettings, PostgresDsn


class Neo4jSettings(BaseSettings):
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    NEO4J_URL: str

    class Config:
        env_file: str = ".env"
