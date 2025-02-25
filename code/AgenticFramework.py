class AgenticFramework:
    
    # Create agent to retrieve number of tables that are relevant to the query
    def retrieve_number_of_tables(self, query: str) -> int:
        pass

    # Create agent to retrieve the schema of the tables
    def retrieve_schemas(self, query: str, numRelevantTables: int) -> str:
        pass

    # Create agent to use the schema to generate a SQL query given a natural language query
    def generate_sql_query(self, query: str, relevant_schemas: str) -> str:
        pass

    # Create agent to execute the SQL query and retrieve the result
    def execute_sql_query(self, query: str) -> str:
        pass

    def pipeline(self, query: str) -> str:
        pass