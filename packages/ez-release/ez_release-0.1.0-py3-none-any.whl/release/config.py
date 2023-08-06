from pydantic import BaseSettings


class Config(BaseSettings):
    domain_separator: str = "/"


config = Config()
