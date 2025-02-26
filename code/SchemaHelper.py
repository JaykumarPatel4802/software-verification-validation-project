from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class SchemaHelper:
    def __init__(self):
        self.vector_store = InMemoryVectorStore(OpenAIEmbeddings(model="text-embedding-3-large"))
        self.all_schemas = []

    def retrieve_all_schemas(self) -> str:
        import os

        schemas_directory = "database/schemas/"
        schemas = []

        for filename in os.listdir(schemas_directory):
            if filename.endswith('.txt'):
                with open(os.path.join(schemas_directory, filename), 'r') as file:
                    schema = file.read()
                    schemas.append(schema)
        
        self.all_schemas = schemas
        return schemas

    def store_schemas(self) -> str:
        schemas = self.retrieve_all_schemas()
        documents = []
        for schema in schemas:
            document = Document(page_content=schema)
            documents.append(document)

        self.vector_store.add_documents(documents=documents)

    def retrieve_relevant_schemas(self, query: str, k: int) -> str:
        relevant_schemas = []
        relevant_documents = self.vector_store.similarity_search(query=query, k=k)
        for doc in relevant_documents:
            relevant_schemas.append(doc.page_content)
        return relevant_schemas
