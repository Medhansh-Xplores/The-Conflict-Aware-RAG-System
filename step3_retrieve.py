import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyDyDgw3qPdwbcznE8KIAdvPT-n5rYC0InM"

%%writefile step3_retrieve.py
"""
STEP 3 — Retrieve + Conflict-Aware Ranking (Google Embeddings, Kaggle-Safe)
"""

import os
import numpy as np
import chromadb
import google.generativeai as genai


# -------------------------------------------
# Require Google API key
# -------------------------------------------
if "GOOGLE_API_KEY" not in os.environ:
    raise EnvironmentError("ERROR: GOOGLE_API_KEY not set. Set it before running Step 3.")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# -------------------------------------------
# Google Embedding Wrapper (same as Step 2)
# -------------------------------------------
class GoogleEmbedder:
    def embed(self, texts):
        vectors = []
        for t in texts:
            resp = genai.embed_content(
                model="models/text-embedding-004",
                content=t
            )
            vectors.append(resp["embedding"])    # 768-dim
        return vectors


# -------------------------------------------
# Cosine similarity
# -------------------------------------------
def cosine_sim(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# -------------------------------------------
# Retrieval + Conflict-Aware Re-ranking
# -------------------------------------------
def retrieve_docs(
    query: str,
    user_role: str,
    persist_dir="./chroma_store",
    top_k=3
):
    # Load vector store
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_collection("nebulagears_policies")

    # Embed the query
    embedder = GoogleEmbedder()
    query_vec = embedder.embed([query])[0]

    # Get stored docs
    results = collection.get(include=["embeddings", "documents", "metadatas"])

    ranked = []

    for idx in range(len(results["ids"])):
        doc_id = results["ids"][idx]
        doc_text = results["documents"][idx]
        metadata = results["metadatas"][idx]

        # Convert role string → list
        roles = metadata.get("applicable_roles", "").split(",")

        # Base similarity
        sim = cosine_sim(query_vec, results["embeddings"][idx])

        # ------------------------
        # Conflict-aware boosts
        # ------------------------

        # 1. Role boost
        role_boost = 1.6 if user_role.lower() in [r.lower() for r in roles] else 1.0

        # 2. Specificity boost (fewer roles = more specific)
        num_roles = max(len(roles), 1)
        specificity_boost = 1.0 + (2.0 / num_roles)

        # 3. Recency boost
        recency_boost = 1.0
        date = metadata.get("date")
        if date:
            year = int(date.split("-")[0])
            recency_boost = 1.0 + (year - 2023) * 0.05

        # Final score
        final_score = sim * role_boost * specificity_boost * recency_boost

        ranked.append({
            "id": doc_id,
            "text": doc_text,
            "metadata": metadata,
            "roles": roles,
            "cosine": sim,
            "final_score": final_score
        })

    # Sort by final score
    ranked_sorted = sorted(ranked, key=lambda x: x["final_score"], reverse=True)

    return ranked_sorted[:top_k]


# -------------------------------------------
# Test Step 3
# -------------------------------------------
if __name__ == "__main__":
    results = retrieve_docs(
        query="I just joined as a new intern. Can I work from home?",
        user_role="intern"
    )

    for d in results:
        print("ID:", d["id"])
        print("Roles:", d["roles"])
        print("Final Score:", d["final_score"])
        print("Text:", d["text"])
        print("-" * 50)

!python step3_retrieve.py
