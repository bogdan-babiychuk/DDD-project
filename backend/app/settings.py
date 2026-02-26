from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent 
ENV_PATH = BASE_DIR / ".env" 

class Config(BaseSettings):
    MONGO_DB_HOST: str
    MONGO_DB_PORT: int
    MONGO_DB_MESSAGE_COLLECTION: str
    MONGO_DB_NAME: str = Field(default="ChatDB")
    MONGO_DB_CHAT_COLLECTION: str

    KAFKA_URL: str
    new_chats_event_topic: str = Field(default='new-chats-topic')
    new_message_event_topic: str = Field(default="new_chat_message-topic")

    model_config = SettingsConfigDict(env_file=ENV_PATH)



    @property
    def MONGO_DB_URL(self):
        return f"mongodb://{self.MONGO_DB_HOST}/{self.MONGO_DB_PORT}"
    

settings = Config()

