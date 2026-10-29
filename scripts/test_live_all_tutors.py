import asyncio
import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.tutor_service import tutor_service
from app.schemas.tutor import TutorRequest

async def main():
    with open('app/data/topics.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    topics = data['topics']

    passed = 0
    failed = 0
    results = []

    print(f"Beginning live verification of {len(topics)} topics...")
    for t in topics:
        tid = t['id']
        parts = t.get('parts', [])
        part_id = parts[0]['id'] if parts else None
        part_name = parts[0]['name'] if parts else "assembly"

        req = TutorRequest(
            topicId=tid,
            partId=part_id,
            question=f"What does {part_name} do?"
        )
        try:
            res = await tutor_service.ask(req)
            if res.answer and len(res.answer) > 15:
                passed += 1
                short_ans = res.answer.replace('\n', ' ')[:90]
                print(f"[PASS] {tid:28} | Part: {part_name:25} | Ans: {short_ans}...")
                results.append({"topicId": tid, "status": "PASS", "answer": res.answer})
            else:
                failed += 1
                print(f"[FAIL EMPTY] {tid}")
                results.append({"topicId": tid, "status": "FAIL_EMPTY"})
        except Exception as e:
            failed += 1
            print(f"[FAIL ERROR] {tid}: {e}")
            results.append({"topicId": tid, "status": "FAIL_ERROR", "error": str(e)})

    print(f"\n==========================================")
    print(f"RESULTS: {passed}/{len(topics)} PASSED | {failed} FAILED")
    print(f"==========================================")
    return passed == len(topics)

if __name__ == '__main__':
    asyncio.run(main())
