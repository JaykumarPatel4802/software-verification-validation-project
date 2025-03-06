from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

llama1b = init_chat_model("llama3.2:1b", model_provider="ollama")
llama8b = init_chat_model("llama3.1:8b", model_provider="ollama")
deepseek = init_chat_model("MFDoom/deepseek-r1-tool-calling:14b", model_provider="ollama")

class GeneratedSQLQuery(BaseModel):
    sql_query: str = Field(description="The generated SQL query")

prompt = "I have a customers table with the column customerId. I want to get the count of all unique customerId's. Can you write me an SQL query to get that?"

s_llama1b = llama1b.with_structured_output(GeneratedSQLQuery)
response1 = s_llama1b.invoke(prompt)
print(response1.sql_query)

s_llama8b = llama8b.with_structured_output(GeneratedSQLQuery)
response8 = s_llama8b.invoke(prompt)
print(response8.sql_query)

s_deepseek = deepseek.with_structured_output(GeneratedSQLQuery)
response_d = s_deepseek.invoke(prompt)
print(response_d.sql_query)