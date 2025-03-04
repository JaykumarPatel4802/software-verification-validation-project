from Text2SQL import Text2SQL, Model
from SQLiteHelper import SQLiteHelper

model = Text2SQL(model=Model.Claude)
# query = model.pipeline("How many distinct artists are there and how many distinct songs are there?")
query = model.pipeline("How many distinct artists are there?")

print("Query:")
print(query)

sqlite_helper = SQLiteHelper()
executionResult = sqlite_helper.executeQuery(query=query)
print(executionResult)

executionResult = sqlite_helper.executeQuery(query="SELECT COUNT(DISTINCT a.ArtistId) as DistinctArtists FROM Artist a;")
print(executionResult)
