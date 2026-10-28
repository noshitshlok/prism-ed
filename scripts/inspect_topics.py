import json

with open("app/data/topics.json", encoding="utf-8") as f:
    topics = json.load(f)

topics_list = topics.get("topics", topics) if isinstance(topics, dict) else topics
print(f"Total topics: {len(topics_list)}")
for t in topics_list:
    print(f"{t['id']} | {t['name']} | {t['discipline']} | modelUrl: {t.get('modelUrl')}")
