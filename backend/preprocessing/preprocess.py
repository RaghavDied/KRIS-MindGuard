from text_cleaning import clean_text

import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

mental_data = load_json("backend/data/mental_health.json")
toxicity_data = load_json("backend/data/toxicity.json")
reddit_data = load_json("backend/data/reddit.json")

def process_mental(data):
    processed = []
    for item in data:
        text = item.get("statement", "").strip()
        label = item.get("status", "").strip()

        if text:
            processed.append({
                "text": clean_text(text),
                "toxicity": None,  # unknown
                "mental_label": label
            })
    return processed


def process_toxicity(data):
    processed = []
    for item in data:
        text = item.get("text", "").strip()
        label = item.get("is_toxic", "").strip()

        if text:
            processed.append({
                "text": clean_text(text),
                "toxicity": 1 if label.lower() == "toxic" else 0,
                "mental_label": None
            })
    return processed


def process_reddit(data):
    processed = []
    for item in data:
        text = item.get("content", "").strip()
        subreddit = item.get("subreddit", "").strip()

        if text:
            processed.append({
                "text": clean_text(text),
                "toxicity": None,
                "mental_label": subreddit  # weak label (use later)
            })
    return processed


mental_clean = process_mental(mental_data)
toxicity_clean = process_toxicity(toxicity_data)
reddit_clean = process_reddit(reddit_data)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

save_json(mental_clean, "backend/data/mental_clean.json")
save_json(toxicity_clean, "backend/data/toxicity_clean.json")
save_json(reddit_clean, "backend/data/reddit_clean.json")

print("Data preprocessing complete!")
print(f"Mental: {len(mental_clean)}")
print(f"Toxicity: {len(toxicity_clean)}")
print(f"Reddit: {len(reddit_clean)}")