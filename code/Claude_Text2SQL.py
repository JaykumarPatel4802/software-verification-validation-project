from AgenticFramework import AgenticFramework
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from SchemaHelper import SchemaHelper
from pydantic import BaseModel, Field
import json
load_dotenv()

class RelevantTablesCount(BaseModel):
    number_of_tables: int = Field(description="The count of the number of relevant tables in the database")

class GeneratedSQLQuery(BaseModel):
    sql_query: str = Field(description="The generated SQL query")

class Claude_Text2SQL(AgenticFramework):

    def __init__(self, is_agentic=False):
        super().__init__()
        self.llm = init_chat_model("claude-3-5-haiku-latest", model_provider="anthropic")
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

        Determine the number of tables in the database that are relevant to the query.
        """
        structured_llm = self.llm.with_structured_output(RelevantTablesCount)
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

        Determine the SQL query that can answer the natural language query.
        """
        structured_llm = self.llm.with_structured_output(GeneratedSQLQuery)
        response = structured_llm.invoke(prompt)
        return response.sql_query
    
    # Create agent to execute the SQL query and retrieve the result
    def save_sql_query(self, query: str, sql_query: str) -> str:
        pass

    def pipeline(self, query: str) -> str:
        if self.is_agentic:
            numRelevantTables = self.retrieve_number_of_tables(query)
            retrievedSchemas = self.retrieve_relevant_schemas(query, numRelevantTables)
            generatedSQLQuery = self.generate_sql_query(query, retrievedSchemas)
        else:
            allSchemas = self.retrieve_all_schemas()
            generatedSQLQuery = self.generate_sql_query(query, allSchemas)
        
        self.save_sql_query(query, generatedSQLQuery)
        return generatedSQLQuery
