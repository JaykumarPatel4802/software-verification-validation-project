from Text2SQL import Text2SQL, Model
from SQLiteHelper import SQLiteHelper
import sqlite3

def execute(q, sqlite_helper, model):
    sql_query = model.pipeline(q)
    if sql_query != None:
        executionResult, error = sqlite_helper.executeQuery(query=sql_query)
    else:
        sql_query, error = "N/A", "Error Generating Query" 
    if error is None:
        return sql_query, str(executionResult)
    else:
        return sql_query, error

def run_benchmark(m, sqlite_helper, iteration, is_agentic = False):
    table_name = 'agentic' if is_agentic else 'agentless'
    query_column, answer_column = None, None
    if m == Model.ChatGPT:
        query_column, answer_column = f"ChatGPT_query{iteration}", f"ChatGPT_result{iteration}"
    elif m == Model.Gemini:
        query_column, answer_column = f"Gemini_query{iteration}", f"Gemini_result{iteration}"
    elif m == Model.Claude:
        query_column, answer_column = f"Claude_query{iteration}", f"Claude_result{iteration}"
    elif m == Model.Llama:
        query_column, answer_column = f"Llama_query{iteration}", f"Llama_result{iteration}"
    elif m == Model.DeepSeek:
        query_column, answer_column = f"DeepSeek_query{iteration}", f"DeepSeek_result{iteration}"
    else:
        return
    
    try:
        with sqlite3.connect("results.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            model = Text2SQL(model=m, is_agentic=is_agentic)
            for row in rows:
                id = row[0]
                question = row[1]
                sql_query, result = execute(question, sqlite_helper, model)
                cursor.execute(f"UPDATE {table_name} SET {query_column} = ?, {answer_column} = ? WHERE id = ?", (sql_query, result, id))
                conn.commit() 
    except Exception as e:
        print("run_benchmark - Failed to connect to database: ", e)

print("Running Agentless")
for m in Model:
    if m == Model.Llama or m == Model.ChatGPT:
        print("Running Model: ", m)
        sqlite_helper = SQLiteHelper()
        for i in range(3):
            run_benchmark(m, sqlite_helper, iteration = i + 1, is_agentic=False)

print("Running Agentic")
for m in Model:
    if m == Model.Llama or m == Model.ChatGPT:
        print("Running Model: ", m)
        sqlite_helper = SQLiteHelper()
        for i in range(3):
            run_benchmark(m, sqlite_helper, iteration = i + 1, is_agentic=True)