from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

class SchemaHelper:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    def get_schema(self, query: str) -> str:
        pass

    def store_document(self, document: str) -> str:
        pass

    def retrieve_all_schemas(self) -> str:
        pass

    def retrieve_relevant_schemas(self, query: str) -> str:
        pass
