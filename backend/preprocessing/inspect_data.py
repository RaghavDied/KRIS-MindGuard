import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

mental = load_json("backend/data/mental_health.json")
toxicity = load_json("backend/data/toxicity.json")
reddit = load_json("backend/data/reddit.json")

print("Mental Health Sample:\n", mental[0])
print("\nToxicity Sample:\n", toxicity[0])
print("\nReddit Sample:\n", reddit[0])