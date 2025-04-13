import json
import random

def sample_by_difficulty(input_file, output_file, x_simple, y_moderate, z_challenging):
    # Load the JSON data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Separate questions by difficulty
    simple = [item for item in data if item["difficulty"] == "simple"]
    moderate = [item for item in data if item["difficulty"] == "moderate"]
    challenging = [item for item in data if item["difficulty"] == "challenging"]

    # Sample from each category
    sampled = []
    sampled += random.sample(simple, min(x_simple, len(simple)))
    sampled += random.sample(moderate, min(y_moderate, len(moderate)))
    sampled += random.sample(challenging, min(z_challenging, len(challenging)))

    # Save to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sampled, f, indent=2)

    print(f"Saved {len(sampled)} samples to {output_file}")

# Example usage
sample_by_difficulty(
    input_file='temp.json',
    output_file='sampled_questions.json',
    x_simple=18,
    y_moderate=9,
    z_challenging=3
)
