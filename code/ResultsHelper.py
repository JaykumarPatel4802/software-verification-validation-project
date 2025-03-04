import sqlite3

database = "results.db"
QuestionsAnswers = {
    "How many distinct artists are there?": "[(275,)]"
}

class ResultsHelper:

    def __init__(self, is_agentic: bool = False):
        self.is_agentic = is_agentic;

    def createDB(self):
        def getCreateTableQuery(is_agentic: bool):
            return f"""
                CREATE TABLE IF NOT EXISTS {'agentic' if is_agentic else 'agentless'} (
                    id INTEGER PRIMARY KEY, 
                    query text NOT NULL, 
                    answer text NOT NULL,
                    ChatGPT_query1 text,
                    ChatGPT_query2 text,
                    ChatGPT_query3 text,
                    ChatGPT_result1 text,
                    ChatGPT_result2 text,
                    ChatGPT_result3 text,
                    Gemini_query1 text,
                    Gemini_query2 text,
                    Gemini_query3 text,
                    Gemini_result1 text,
                    Gemini_result2 text,
                    Gemini_result3 text,
                    Claude_query1 text,
                    Claude_query2 text,
                    Claude_query3 text,
                    Claude_result1 text,
                    Claude_result2 text,
                    Claude_result3 text
                );
                """

        def createTables(conn):
            cursor = conn.cursor()
            cursor.execute(getCreateTableQuery(is_agentic=False))
            cursor.execute(getCreateTableQuery(is_agentic=True))
            conn.commit()

        try:
            with sqlite3.connect(database) as conn:
                createTables(conn)
        except Exception as e:
            print("Failed to connect to database: ", e)

    def loadQueriesAnswers(self):
        def getCreateTableQuery(is_agentic: bool):
            return f"""
                INSERT INTO {'agentic' if is_agentic else 'agentless'} (query, answer) VALUES (?, ?);
                """
        
        def addQuestionAnswer(conn, question, answer):    
            cursor = conn.cursor()
            cursor.execute(getCreateTableQuery(is_agentic=False), (question, answer))
            cursor.execute(getCreateTableQuery(is_agentic=True), (question, answer))
            conn.commit()

        try:
            with sqlite3.connect(database) as conn:
                for question in QuestionsAnswers:
                    answer = QuestionsAnswers[question]
                    addQuestionAnswer(conn, question, answer)
        except Exception as e:
            print("Failed to connect to database: ", e)

    def setupDB(self):
        self.createDB()
        self.loadQueriesAnswers()