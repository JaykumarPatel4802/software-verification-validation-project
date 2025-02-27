from ChatGPT_Text2SQL import ChatGPT_Text2SQL
from SQLiteHelper import SQLiteHelper
gpt = ChatGPT_Text2SQL()
query = gpt.pipeline("How many distinct artists are there and how many distinct songs are there?")

print("Query:")
print(query)

sqlite_helper = SQLiteHelper()
executionResult = sqlite_helper.executeQuery(query=query)
print(executionResult)

executionResult = sqlite_helper.executeQuery(query="SELECT COUNT(DISTINCT a.ArtistId) as DistinctArtists FROM Artist a;")
print(executionResult)
