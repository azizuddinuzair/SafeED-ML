import pytest
from difflib import SequenceMatcher

def normalize(q):
    return q.strip().lower()


"""
Run command: pytest safeEd_ML/tests/test_dupes.py

Test case dictionary:
no_exact_duplicates: Ensure dataset has minimal exact duplicate queries.
paraphrased_variations: Ensure multiple paraphrased variations exist for key intents.
no_too_many_duplicates: Ensure total exact duplicates are below a threshold.
keep_similar_surface_forms: Ensure specific paraphrased surface forms are present.
metadata_fields_present: Ensure all required metadata fields are present in each entry.
metadata_types_and_values: Ensure metadata fields have correct types and valid values. 
semantic_clustering: Ensure semantic clustering reveals healthy paraphrase groups.
category_variance: Ensure categories have sufficient representation.
"""

def test_no_exact_duplicates():
    from safeEd_ML.data_loader import load_dataset # Loads your list-of-dict queries
    data = load_dataset()
    queries = [normalize(q['query']) for q in data]
    duplicates = set([q for q in queries if queries.count(q) > 1])
    # Assert that the percent of duplicates is below a threshold (e.g., <2%)
    assert len(duplicates) / len(queries) < 0.02, f"Too many exact duplicates: {duplicates}"


def similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a, b).ratio() > threshold

def test_paraphrased_variations():
    from safeEd_ML.data_loader import load_dataset
    data = load_dataset()
    canonical = "Can I get pregnant from pre-cum?"
    # Normalize queries for better matching
    found = [q for q in data if similar(canonical.strip().lower(), q['query'].strip().lower(), threshold=0.65)]
    # Check that we have multiple variations
    assert len(found) >= 3, "Not enough paraphrased variations for this intent"

def test_no_too_many_duplicates():
    from safeEd_ML.data_loader import load_dataset
    data = load_dataset()
    queries = [q['query'].strip().lower() for q in data]
    exact_dupes = len(queries) - len(set(queries))
    assert exact_dupes < 10, f"Dataset has {exact_dupes} exact duplicate queries!"


def test_keep_similar_surface_forms():
    from safeEd_ML.data_loader import load_dataset
    import difflib
    data = load_dataset()
    intents = [
        "Can I get HIV from kissing?",
        "Can you get HIV from kissing?",
        "Is HIV transmissible through kissing?",
    ]
    queries = [q['query'].strip().lower() for q in data]
    # Make sure all these surface forms are present
    for intent in intents:
        matches = [q for q in queries if difflib.SequenceMatcher(None, q, intent.lower()).ratio() > 0.7]
        assert matches, f"Missing paraphrase for: {intent}"


# --- Metadata validation tests ---
def test_metadata_fields_present():
    from safeEd_ML.data_loader import load_dataset
    data = load_dataset()
    required_fields = ["query", "label", "source", "date", "category", "reviewed", "notes"]
    for i, entry in enumerate(data):
        for field in required_fields:
            assert field in entry, f"Missing field '{field}' in entry {i}: {entry}"

def test_metadata_types_and_values():
    from safeEd_ML.data_loader import load_dataset
    import datetime
    data = load_dataset()
    allowed_sources = {"manual", "crowdsourced", "copilot_generated", "web_scraped"}
    for i, entry in enumerate(data):
        # reviewed must be boolean
        assert isinstance(entry["reviewed"], bool), f"'reviewed' not bool in entry {i}: {entry}"
        # date must be valid ISO format
        try:
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d")
        except Exception:
            assert False, f"Invalid date format in entry {i}: {entry['date']}"
        # source must be in allowed list
        assert entry["source"] in allowed_sources, f"Invalid source in entry {i}: {entry['source']}"
        # category must be non-empty string
        assert isinstance(entry["category"], str) and entry["category"].strip(), f"Missing/empty category in entry {i}: {entry['category']}"
        # notes must be string (can be empty)
        assert isinstance(entry["notes"], str), f"Notes not string in entry {i}: {entry['notes']}"


# --- Advanced semantic clustering test ---
def test_query_clusters():
    from safeEd_ML.data_loader import load_dataset
    data = load_dataset()
    queries = [q['query'] for q in data]
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.cluster import AgglomerativeClustering
    except ImportError:
        pytest.skip("sentence-transformers and scikit-learn required for semantic clustering test.")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(queries)
    n_clusters = max(2, len(queries) // 10)
    clustering = AgglomerativeClustering(n_clusters=n_clusters)
    cluster_labels = clustering.fit_predict(embeddings)
    from collections import Counter
    cluster_sizes = Counter(cluster_labels)
    # This checks for at least SOME clusters > 2 members, not just singletons
    assert any(size > 2 for size in cluster_sizes.values()), f"No clusters have healthy paraphrase groups: {cluster_sizes}"
    print(f"Cluster sizes: {cluster_sizes}")

# --- Category variance test ---
def test_category_variance():
    from safeEd_ML.data_loader import load_dataset
    data = load_dataset()
    categories = [q.get('category', 'unknown') for q in data]
    from collections import Counter
    cat_counts = Counter(categories)
    print("Category counts:", cat_counts)
    # Alert if any category has fewer than 5 queries
    for cat, count in cat_counts.items():
        assert count >= 5, f"Category '{cat}' underrepresented ({count} entries)"
