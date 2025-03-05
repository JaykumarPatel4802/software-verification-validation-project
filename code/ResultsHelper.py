from QuestionsAnswers import QuestionsAnswers
import sqlite3

results_database = "results.db"
source_database = "database/Chinook_Sqlite.sqlite"

class ResultsHelper:

    def __init__(self, is_agentic: bool = False):
        self.is_agentic = is_agentic

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
                    Claude_result3 text,
                    Llama_query1 text,
                    Llama_query2 text,
                    Llama_query3 text,
                    Llama_result1 text,
                    Llama_result2 text,
                    Llama_result3 text,
                    DeepSeek_query1 text,
                    DeepSeek_query2 text,
                    DeepSeek_query3 text,
                    DeepSeek_result1 text,
                    DeepSeek_result2 text,
                    DeepSeek_result3 text
                );
                """
        
        def deleteTables(conn):
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS agentic;")
            cursor.execute("DROP TABLE IF EXISTS agentless;")
            conn.commit()

        def createTables(conn):
            cursor = conn.cursor()
            cursor.execute(getCreateTableQuery(is_agentic=False))
            cursor.execute(getCreateTableQuery(is_agentic=True))
            conn.commit()

        try:
            with sqlite3.connect(results_database) as conn:
                deleteTables(conn)
                createTables(conn)
        except Exception as e:
            print("createDB - Failed to connect to database: ", e)

    def loadQuestionsAnswers(self):
        def clearTables(conn):
            cursor = conn.cursor()
            cursor.execute("DELETE FROM agentic")
            cursor.execute("DELETE FROM agentless")
            conn.commit()

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
            with sqlite3.connect(results_database) as conn:
                clearTables(conn)
                for question in QuestionsAnswers:
                    answer = QuestionsAnswers[question]["Answer"]
                    addQuestionAnswer(conn, question, answer)
        except Exception as e:
            print("loadQuestionsAnswers - Failed to connect to database: ", e)
    
    def determineQuestionsAnswers(self):

        def executeQuery(conn, query):
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

        try:
            with sqlite3.connect(source_database) as conn:
                for question in QuestionsAnswers:
                    query = QuestionsAnswers[question]["SQL_Query"]
                    answer = executeQuery(conn, query)
                    QuestionsAnswers[question]["Answer"] = str(answer)

        except Exception as e:
            print("determineQuestionsAnswers - Failed to connect to database: ", e)

    def setupDB(self):
        self.createDB()
        self.loadQuestionsAnswers()