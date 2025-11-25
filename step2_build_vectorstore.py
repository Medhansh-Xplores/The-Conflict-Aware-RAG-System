import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyDyDgw3qPdwbcznE8KIAdvPT-n5rYC0InM"

%%writefile step2_build_vectorstore.py
"""
STEP 2 — Build Vector Store using Google Embeddings (Kaggle-Compatible)
"""

import json
import os
import chromadb
import google.generativeai as genai

# -------------------------------------------
# Verify & load Google API Key
# -------------------------------------------
if "GOOGLE_API_KEY" not in os.environ:
    raise EnvironmentError(
        "GOOGLE_API_KEY not found. Run: os.environ['GOOGLE_API_KEY'] = 'yourkey'"
    )

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# -------------------------------------------
# Load JSONL
# -------------------------------------------
def load_jsonl(path="prepared_docs.jsonl"):
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))
    return docs


# -------------------------------------------
# Google Embedding Wrapper (Kaggle API)
# -------------------------------------------
class GoogleEmbedder:
    def embed(self, texts):
        vectors = []
        for t in texts:
            resp = genai.embed_content(
                model="models/text-embedding-004",
                content=t
            )
            vectors.append(resp["embedding"])   # 768-dimensional vector
        return vectors


# -------------------------------------------
# Build Chroma Vector Store
# -------------------------------------------
def build_vectorstore(jsonl_path="prepared_docs.jsonl", persist_dir="./chroma_store"):

    print("📂 Loading prepared document chunks...")
    docs = load_jsonl(jsonl_path)
    print(f"Loaded {len(docs)} chunks.")

    print("\n🔢 Generating Google Embeddings (768 dimensions)...")
    embedder = GoogleEmbedder()
    texts = [d["text"] for d in docs]
    embeddings = embedder.embed(texts)

    print("\n🗄 Creating ChromaDB (persistent)...")
    client = chromadb.PersistentClient(path=persist_dir)

    collection = client.get_or_create_collection(
        name="nebulagears_policies",
        metadata={"hnsw:space": "cosine"}  # use cosine similarity
    )

    print("📝 Inserting embedding records into ChromaDB...")

    # Metadata fix (Chroma does not allow lists)
    safe_metadatas = []
    for d in docs:
        fixed = {}
        for k, v in d["metadata"].items():
            fixed[k] = ",".join(v) if isinstance(v, list) else v
        safe_metadatas.append(fixed)

    collection.add(
        ids=[d["id"] for d in docs],
        embeddings=embeddings,
        documents=texts,
        metadatas=safe_metadatas
    )

    print("\n✅ SUCCESS! Vector store built and saved at:", persist_dir)
    return collection


# -------------------------------------------
# Run Step 2
# -------------------------------------------
if __name__ == "__main__":
    build_vectorstore()
