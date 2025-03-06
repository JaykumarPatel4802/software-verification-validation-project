from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from SchemaHelper import SchemaHelper
from pydantic import BaseModel, Field
import vertexai
import json
from enum import Enum
load_dotenv()


# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
# llm = init_chat_model("gemini-1.5-flash", model_provider="google_vertexai")
llm = init_chat_model("claude-3-haiku-20240307", model_provider="anthropic")
# llm = init_chat_model("llama3.1:8b", model_provider="ollama")
# llm = init_chat_model("MFDoom/deepseek-r1-tool-calling:14b", model_provider="ollama")

response = llm.invoke("Hi")
print(response)