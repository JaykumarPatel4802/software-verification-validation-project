from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
load_dotenv()

class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")

# model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, response_format={"type": "json_object"})
model = init_chat_model("gpt-4o-mini", model_provider="openai", response_format={"type": "json_object"})

# Prompt must explicitly state JSON
response = model.invoke("Tell me a joke about cats in JSON format")

# structured_llm = model.with_structured_output(Joke)
# response = structured_llm.invoke("Tell me a joke about cats")

print(f"Response: {response}")