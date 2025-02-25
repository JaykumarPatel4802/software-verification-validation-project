from AgenticFramework import AgenticFramework
from langchain.chat_models import init_chat_model
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

class Llama_Text2SQL(AgenticFramework):

    def __init__(self):
        super().__init__()
        self.llm = init_chat_model("llama3.1:8b", model_provider="ollama")

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


