from ChatGPT_Text2SQL import ChatGPT_Text2SQL
from Gemini_Text2SQL import Gemini_Text2SQL
from Claude_Text2SQL import Claude_Text2SQL
from SQLiteHelper import SQLiteHelper

# model = ChatGPT_Text2SQL()
model = Gemini_Text2SQL()
# model = Claude_Text2SQL()
query = model.pipeline("How many distinct artists are there and how many distinct songs are there?")

print("Query:")
print(query)

sqlite_helper = SQLiteHelper()
executionResult = sqlite_helper.executeQuery(query=query)
print(executionResult)

executionResult = sqlite_helper.executeQuery(query="SELECT COUNT(DISTINCT a.ArtistId) as DistinctArtists FROM Artist a;")
print(executionResult)
