from AgenticFramework import AgenticFramework
from langchain.chat_models import init_chat_model
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

class Gemini_Text2SQL(AgenticFramework):

    def __init__(self):
        super().__init__()
        self.llm = llm = init_chat_model("gemini-2.0-flash-001", model_provider="google_vertexai")

    # Create agent to retrieve number of tables that are relevant to the query
    def retrieve_number_of_tables(self, query: str) -> int:
        pass

    # Create agent to retrieve the schema of the tables
    def retrieve_schema(self, query: str, contextCount: int) -> str:
        pass

    # Create agent to use the schema to generate a SQL query given a natural language query
    def generate_sql_query(self, query: str, schema: str) -> str:
        pass

    def pipeline(self, query: str) -> str:
        numRelevantTables = self.retrieve_number_of_tables(query)
        retrievedSchema = self.retrieve_schema(query, numRelevantTables)
        generatedSQLQuery = self.generate_sql_query(query, retrievedSchema)
        executionResult = self.execute_sql_query(generatedSQLQuery)
        return executionResult


    # Create agent to execute the SQL query and retrieve the result
    def execute_sql_query(self, query: str) -> str:
        pass

    # Create agent to evaluate the result of the SQL query
    def evaluate_sql_query(self, query: str, result: str) -> str:
        pass


