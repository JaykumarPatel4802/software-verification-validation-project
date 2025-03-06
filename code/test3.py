from Text2SQL import Text2SQL
from Text2SQL import Model

model = Text2SQL(model=Model.Claude, is_agentic=True)
query, error = model.pipeline("Determine the number of artists.")
print(query)
print(error)
