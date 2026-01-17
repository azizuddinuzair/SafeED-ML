from query_constants import DEFAULT_SKIP
import json
import os

LABEL_OPTIONS = [
    "question",
    "belief/claim/statement",
    "needs verification",
    "concern/urgent"
]

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'queries.json')

def load_queries():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_queries(queries):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(queries, f, indent=2, ensure_ascii=False)

def review_labels(skip=0):
    queries = load_queries()
    total = len(queries)
    print(f"Loaded {total} queries. Skipping first {skip}.")
    for i, q in enumerate(queries[skip:], start=skip):
        print(f"\nQuery {i+1}/{total}:")
        print(f"  {q['query']}")
        current_label = q.get('label', '')
        if isinstance(current_label, list):
            print(f"  Current labels: {', '.join(current_label)}")
        else:
            print(f"  Current label: {current_label}")
        print(f"  Notes: {q.get('notes', '')}")
        print("  Options:")
        for idx, opt in enumerate(LABEL_OPTIONS, 1):
            print(f"    {idx}. {opt}")
        ans = input("Choose new label(s) (comma-separated 1-4, Enter to keep current): ").strip()
        if ans:
            try:
                indices = [int(x)-1 for x in ans.split(',') if x.strip().isdigit() and 0 < int(x) <= len(LABEL_OPTIONS)]
                new_labels = [LABEL_OPTIONS[idx] for idx in indices]
                if new_labels:
                    q['label'] = new_labels if len(new_labels) > 1 else new_labels[0]
                    print(f"Label(s) updated to: {q['label']}")
                else:
                    print("No valid selection, label unchanged.")
            except Exception as e:
                print(f"Error: {e}. Label unchanged.")
        else:
            print("Label unchanged.")
        queries[i] = q
        save_queries(queries)
        print("Saved.")

if __name__ == "__main__":
    import sys
    skip = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SKIP
    review_labels(skip=skip)
