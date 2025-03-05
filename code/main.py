from Text2SQL import Text2SQL, Model
from SQLiteHelper import SQLiteHelper

def execute(m, q):
    model = Text2SQL(model=m)
    sql_query = model.pipeline(q)
    sqlite_helper = SQLiteHelper()
    executionResult, error = sqlite_helper.executeQuery(query=sql_query)
    if error is None:
        print(executionResult)
    else:
        print(error)

queries = [
    "How many artists and customers are there?",
    "What are the top 5 countries with the most Invoices?",
    "What is the first and last name of the customer who spent the most money, and what was the amount they spent?",
    "Who is the biggest fan for each artist? In order words, for each artist, which customer bought most of their tracks?"
]

# queries = [
#     "How many artists and customers are there?",
#     "What are the top 5 countries with the most Invoices?"
# ]

for m in Model:
    print(m)
    for q in queries:
        execute(m, q)