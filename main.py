"""
main.py
Run the complete Conflict-Aware RAG pipeline end-to-end.

This script:
1. Prepares the data
2. Builds the ChromaDB vector store
3. Retrieves documents using conflict-aware ranking
4. Generates the final answer using Gemini Flash
"""

from step1_prepare_data import prepare_step1
from step2_build_vectorstore import build_vectorstore
from step3_retrieve import retrieve_docs
from step4_answer import generate_answer


def run_pipeline():
    print("\n==============================")
    print(" STEP 1 — Preparing Documents ")
    print("==============================")
    prepare_step1()

    print("\n==============================")
    print(" STEP 2 — Building Vector Store ")
    print("==============================")
    build_vectorstore()

    print("\n==============================")
    print(" STEP 3 — Conflict-Aware Retrieval ")
    print("==============================")
    query = "I just joined as a new intern. Can I work from home?"
    user_role = "intern"

    ranked_docs = retrieve_docs(
        query=query,
        user_role=user_role
    )

    print("\nTop-ranked documents:")
    for i, d in enumerate(ranked_docs, start=1):
        print(f"\n--- Document {i} ---")
        print("ID:", d["id"])
        print("Roles:", d["roles_list"])
        print("Final Score:", d["final_score"])

    print("\n==============================")
    print(" STEP 4 — Generating Final Answer ")
    print("==============================")
    final_answer = generate_answer(
        query=query,
        user_role=user_role,
        ranked_docs=ranked_docs
    )

    print("\n==============================")
    print("      Pipeline Complete       ")
    print("==============================")
    return final_answer


if __name__ == "__main__":
    run_pipeline()
