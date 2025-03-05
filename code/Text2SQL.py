from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from SchemaHelper import SchemaHelper
from pydantic import BaseModel, Field
import vertexai
import json
from enum import Enum
load_dotenv()

class Model(Enum):
    Llama = 1
    ChatGPT = 2
    Gemini = 3
    Claude = 4
    DeepSeek = 5

class RelevantTablesCount(BaseModel):
    number_of_tables: int = Field(description="The count of the number of relevant tables in the database")

class GeneratedSQLQuery(BaseModel):
    sql_query: str = Field(description="The generated SQL query")

class Text2SQL():

    def __init__(self, model: Model = Model.ChatGPT, is_agentic: bool = False):
        if model == Model.ChatGPT:
            self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        elif model == Model.Gemini:
            self.llm = init_chat_model("gemini-1.5-flash", model_provider="google_vertexai")
        elif model == Model.Claude:
            self.llm = init_chat_model("claude-3-haiku-20240307", model_provider="anthropic")
        elif model == Model.Llama:
            # self.llm = init_chat_model("llama3-8b-8192", model_provider="groq")
            # self.llm = init_chat_model("llama3.2:1b", model_provider="ollama")
            self.llm = init_chat_model("llama3.1:8b", model_provider="ollama")
        elif model == Model.DeepSeek:
            self.llm = init_chat_model("MFDoom/deepseek-r1-tool-calling:14b", model_provider="ollama")
        else:
            self.llm = None
        self.sh = SchemaHelper()
        self.sh.store_schemas()
        self.is_agentic = is_agentic

    # Create agent to retrieve number of tables that are relevant to the query
    def retrieve_number_of_tables(self, query: str) -> int:
        allSchemas = self.sh.all_schemas
        prompt = f"""
        You are a helpful assistant that retrieves the number of tables in a database that are relevant to the query.
        The query is: {query}
        The schemas of the tables in the database are: {allSchemas}

        Determine the number of tables in the database that are relevant to the query. If you aren't sure, provide your best guess.
        """
        structured_llm = self.llm.with_structured_output(RelevantTablesCount)
        # structured_llm = self.llm.with_structured_output(RelevantTablesCount, method="json_mode") # https://python.langchain.com/v0.1/docs/modules/model_io/chat/structured_output/
        response = structured_llm.invoke(prompt)
        return response.number_of_tables


    # Create agent to retrieve the relevant schemas of the tables
    def retrieve_relevant_schemas(self, query: str, contextCount: int) -> str:
        relevantSchemas = self.sh.retrieve_relevant_schemas(query, contextCount)
        joinedRelevantSchemas = "\n\n----------\n\n".join(relevantSchemas)
        return joinedRelevantSchemas
    
    # Create agent to retrieve al schemas of the tables
    def retrieve_all_schemas(self) -> str:
        relevantSchemas = self.sh.retrieve_all_schemas()
        joinedAllSchemas = "\n\n----------\n\n".join(relevantSchemas)
        return joinedAllSchemas

    # Create agent to use the schema to generate a SQL query given a natural language query
    def generate_sql_query(self, query: str, relevant_schemas: str) -> str:
        prompt = f"""
        You are a helpful assistant that generates a SQL query given a natural language query and a list of relevant schemas.
        The query is: {query}
        The relevant schemas are: {relevant_schemas}

        Determine the SQL query that can answer the natural language query. Only generate one SQL query. If you aren't sure, provide your best guess.
        """
        structured_llm = self.llm.with_structured_output(GeneratedSQLQuery)
        response = structured_llm.invoke(prompt)
        return response.sql_query

    def pipeline(self, query: str) -> str:
        try:
            if self.is_agentic:
                numRelevantTables = self.retrieve_number_of_tables(query)
                retrievedSchemas = self.retrieve_relevant_schemas(query, numRelevantTables)
                generatedSQLQuery = self.generate_sql_query(query, retrievedSchemas)
            else:
                allSchemas = self.retrieve_all_schemas()
                generatedSQLQuery = self.generate_sql_query(query, allSchemas)
        
            return generatedSQLQuery, None
        except Exception as e:
            return None, str(e)