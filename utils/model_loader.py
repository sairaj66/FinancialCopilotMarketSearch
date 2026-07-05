import os
from typing import Any, Literal, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from utils.config_loader import load_config

load_dotenv()


class ConfigLoader:
    def __init__(self):
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    """Loads the selected chat model and keeps provider switching simple."""

    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        provider = os.getenv("MODEL_PROVIDER", self.model_provider).lower()

        if provider == "groq":
            from langchain_groq import ChatGroq

            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

            model_name = self.config["llm"]["groq"]["model_name"]
            temperature = self.config["llm"]["groq"].get("temperature", 0.1)
            return ChatGroq(model=model_name, api_key=api_key, temperature=temperature)

        if provider == "openai":
            from langchain_openai import ChatOpenAI

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

            model_name = self.config["llm"]["openai"]["model_name"]
            temperature = self.config["llm"]["openai"].get("temperature", 0.1)
            return ChatOpenAI(model=model_name, api_key=api_key, temperature=temperature)

        raise ValueError(f"Unsupported model provider: {provider}")
