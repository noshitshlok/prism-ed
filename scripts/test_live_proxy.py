import urllib.request
import json

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

ready_topics = get_json("http://localhost:5173/api/v1/topics")
print(f"READY TOPICS IN DEMO: {len(ready_topics)}")
for t in ready_topics:
    print(f"  * {t['id']}: {t['name']} | source: {t.get('modelSource')}")

all_topics = get_json("http://localhost:5173/api/v1/topics?include_all=true")
print(f"TOTAL REGISTERED TOPICS: {len(all_topics)}")

print("\nVerifying 3D model asset delivery via Vite proxy:")
for t in ready_topics:
    detail = get_json(f"http://localhost:5173/api/v1/topics/{t['id']}")
    model_url = "http://localhost:5173" + detail["modelUrl"]
    with urllib.request.urlopen(model_url) as resp:
        content_len = len(resp.read())
        print(f"  OK {t['id']}: {content_len} bytes ({round(content_len/1024, 1)} KB)")

print("\nALL VERIFICATIONS PASSED!")
