import os
from dotenv import load_dotenv
from pydantic import BaseModel


class EnvironmentSettings(BaseModel):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    HASHING_ALGORITHM: str

    @classmethod
    def load_settings(cls):
        load_dotenv()
        data = {}
        for field_key in EnvironmentSettings.model_fields.keys():
            data.update({field_key: os.getenv(field_key)})
        return cls(**data)


Settings = EnvironmentSettings.load_settings()
