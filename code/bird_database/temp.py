import json
import random


input_file = "sampled_questions.json"
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    print(item["question"])