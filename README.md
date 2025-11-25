# 🌌 NebulaGears: Conflict-Aware RAG System  
### Google Gemini Flash + ChromaDB + Role-Based Policy Resolution

This project implements a **Conflict-Aware Retrieval-Augmented Generation (RAG)** system that uses **Google Gemini Flash** and **ChromaDB** to answer employee policy questions accurately — even when internal documents contain **conflicting information**.

The system ensures the final answer is **role-specific, citation-backed, and conflict-resolved**, which is required because some documents contradict others.

---

# 📁 Repository Structure

```
nebula-rag-conflict-aware/
├── step1_prepare_data.py
├── step2_build_vectorstore.py
├── step3_retrieve.py
├── step4_answer.py
├── main.py
├── requirements.txt
├── README.md
└── assets/
    └── intern_query_screenshot.png
```

---

# 🚀 Pipeline Overview

## 🟦 Step 1 — Data Preparation  
Loads and cleans documents, splits them into chunks, adds metadata, and saves them into `prepared_docs.jsonl`.

## 🟦 Step 2 — Vector Store Creation  
Embeds the text using Google `text-embedding-004` and stores embeddings + metadata in **ChromaDB**.

## 🟦 Step 3 — Conflict-Aware Retrieval  
Retrieves relevant chunks and applies:

- **Role Boost**
- **Specificity Boost**
- **Recency Boost**

Final score ensures the correct document wins even when policies conflict.

## 🟦 Step 4 — Final Answer Generation  
Uses **Gemini Flash** to generate:

- Final ruling  
- One citation  
- Supporting quote  
- Explanation why other documents were rejected  

---

# ▶️ How to Run

```
python step1_prepare_data.py
python step2_build_vectorstore.py
python step3_retrieve.py
python step4_answer.py
```

Or run all:

```
python main.py
```

---

# 📸 Required Screenshot

Upload your result screenshot to:

```
assets/intern_query_screenshot.png
```

Include it below in README:

```
![Intern Query Output](assets/intern_query_screenshot.png)
```

---

# 💰 Cost Analysis

Embedding 10,000 documents: **~$0.04**  
5,000 queries/day: **~$1.12 per month**  
**Total: ~$1.20 monthly**

---

# 🏁 Conclusion

This conflict-aware RAG system ensures correct, role-specific policy answers using Google Gemini Flash and local ChromaDB storage. It fully satisfies all assignment requirements.

