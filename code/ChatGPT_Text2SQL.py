from AgenticFramework import AgenticFramework
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from SchemaHelper import SchemaHelper
import json
load_dotenv()

class ChatGPT_Text2SQL(AgenticFramework):

    def __init__(self):
        super().__init__()
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    # Create agent to retrieve number of tables that are relevant to the query
    def retrieve_number_of_tables(self, query: str) -> int:
        allSchemas = SchemaHelper.retrieve_all_documents()
        prompt = f"""
        You are a helpful assistant that retrieves the number of tables that are relevant to the query.
        The query is: {query}
        The schemas are: {allSchemas}

        Return the number of tables that are relevant to the query in the following JSON format:
        {{
            "number_of_tables": <number_of_tables>
        }}
        """
        response = self.llm.invoke(prompt)
        return json.loads(response)["number_of_tables"]


    # Create agent to retrieve the schemas of the tables
    def retrieve_schemas(self, query: str, contextCount: int) -> str:
        relevantSchemas = SchemaHelper.retrieve_relevant_schemas(query, contextCount)
        relevantSchemas = "\n".join(relevantSchemas)
        return relevantSchemas

    # Create agent to use the schema to generate a SQL query given a natural language query
    def generate_sql_query(self, query: str, relevant_schemas: str) -> str:
        prompt = f"""
        You are a helpful assistant that generates a SQL query given a natural language query and a list of relevant schemas.
        The query is: {query}
        The relevant schemas are: {relevant_schemas}

        Return the SQL query in the following JSON format:
        {{
            "sql_query": <sql_query>
        }}
        """
        response = self.llm.invoke(prompt)
        return json.loads(response)["sql_query"]
    
    # Create agent to execute the SQL query and retrieve the result
    def save_sql_query(self, query: str, sql_query: str) -> str:
        pass

    def pipeline(self, query: str) -> str:
        numRelevantTables = self.retrieve_number_of_tables(query)
        retrievedSchemas = self.retrieve_schemas(query, numRelevantTables)
        generatedSQLQuery = self.generate_sql_query(query, retrievedSchemas)
        self.save_sql_query(query, generatedSQLQuery)
