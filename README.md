# NebulaGears: Conflict-Aware RAG System
### Google Gemini Flash + ChromaDB + Role-Based Policy Resolution

This project implements a **Conflict-Aware Retrieval-Augmented Generation (RAG)** pipeline that uses **Google Gemini Flash** and **ChromaDB** to answer employee policy questions based on internal company documents — even when those documents contain **contradictory rules**.

## Project Structure
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

## Pipeline Overview

### Step 1 — Data Preparation
Prepares and structures policy documents into `prepared_docs.jsonl` with metadata.

### Step 2 — Vector Store
Embeds documents using Google `text-embedding-004` and stores them in ChromaDB.

### Step 3 — Conflict-Aware Retrieval
Ranks documents using cosine similarity + role boost + specificity boost + recency boost.

### Step 4 — Final Answer Generation
Uses Gemini Flash to generate a fully cited, role-correct final answer.

## Cost Analysis
Embedding 10,000 documents ≈ **$0.04** (one-time)  
Handling 5,000 daily queries ≈ **$1.12/month**

## Screenshot
Insert your screenshot inside:
`assets/intern_query_screenshot.png`
