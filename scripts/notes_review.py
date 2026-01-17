from query_constants import DEFAULT_SKIP
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'queries.json')

def load_queries():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_queries(queries):
    print(f"[DEBUG] Attempting to save to: {DATA_PATH}")
    try:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(queries, f, indent=2, ensure_ascii=False)
        print("[DEBUG] Save successful.")
    except Exception as e:
        print(f"[ERROR] Failed to save queries: {e}")

def review_notes(skip=0):
    queries = load_queries()
    total = len(queries)
    print(f"Loaded {total} queries. Skipping first {skip}.")
    print(f"[DEBUG] Data path in use: {DATA_PATH}")
    for i, q in enumerate(queries[skip:], start=skip):
        qtext = q.get('query') or q.get('text')
        print(f"\nQuery {i+1}/{total}:")
        print(f"  {qtext}")
        print(f"  Current notes: {q.get('notes', '')}")
        new_notes = input("Edit notes (Enter to keep current): ").strip()
        if new_notes:
            q['notes'] = new_notes
            print("Notes updated.")
        else:
            print("Notes unchanged.")
        queries[i] = q
    print("[DEBUG] Calling save_queries...")
    save_queries(queries)
    print("All notes saved.")

if __name__ == "__main__":
    import sys
    skip = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SKIP
    review_notes(skip=skip)
