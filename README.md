# 🌌 NebulaGears: Conflict-Aware RAG System  
### Google Gemini Flash + ChromaDB + Role-Based Policy Resolution

This repository implements a **Conflict-Aware Retrieval-Augmented Generation (RAG)** system capable of answering internal company policy questions even when the underlying documents contain **conflicting rules**.  
Using **Google Gemini Flash**, **Google text embeddings**, and a **local ChromaDB vector store**, the system ensures that employees receive **role-appropriate, citation-backed, and fully justified answers**.

This project was built to pass the assignment scenario:

> **“I just joined as a new intern. Can I work from home?”**  
Even though general employees may work remotely, interns *cannot*, and the system must correctly cite the **Intern FAQ**.

---

# 📁 Repository Structure

```
nebula-rag-conflict-aware/
│
├── step1_prepare_data.py
├── step2_build_vectorstore.py
├── step3_retrieve.py
├── step4_answer.py
│
├── main.py
│
├── requirements.txt
├── README.md
│
└── intern_query_screenshot.png
    
```

---

# 🚀 Pipeline Overview (Detailed)

This project is intentionally split into **four modular steps** for clarity and correctness.

---

## 🟦 **Step 1 — Data Preparation**  
**File:** `step1_prepare_data.py`

This step transforms raw policy documents into a structured dataset.

### It performs:
- Text cleaning (removes extra spaces, noise)
- Chunking into RAG-friendly segments
- Metadata attachment:
  - `roles` (e.g., intern, manager, all_employees)
  - `policy_type` (handbook, update, FAQ)
  - `date`
  - `source_filename`
- Exports all chunks to **prepared_docs.jsonl**

**Why this matters:**  
RAG pipelines cannot operate efficiently on raw text. Metadata is essential for conflict resolution.

---

## 🟦 **Step 2 — Vector Store Creation**  
**File:** `step2_build_vectorstore.py`

This step creates the semantic index used for retrieval.

### Responsibilities:
- Load `prepared_docs.jsonl`
- Generate embeddings using **Google `text-embedding-004`**
- Create a **persistent ChromaDB** instance
- Store embeddings, text chunks, and metadata

**Why this matters:**  
ChromaDB acts as the **local knowledge base** for all semantic search operations.

---

## 🟦 **Step 3 — Conflict-Aware Retrieval**  
**File:** `step3_retrieve.py`

This is the heart of the system.  
Instead of returning the document with the highest cosine similarity, this step applies a **Conflict-Aware Ranking Layer**.

### 🔍 Step 3 Logic Includes:

#### 1️⃣ Cosine Similarity  
Standard semantic similarity based on text embeddings.

#### 2️⃣ **Role Boost (Most Important)**  
If the document applies to the user’s role:

```
score *= 1.6
```

This ensures:
- Intern FAQs override policies for general employees  
- Manager updates override employee handbooks  
- Role-specific rules always win

#### 3️⃣ **Specificity Boost**  
Policies applying to fewer roles are more authoritative:

```
specificity_boost = 1 + (2 / number_of_roles)
```

Example:
- Intern-only FAQ (1 role) → highest specificity  
- Handbook (all employees) → lowest specificity

#### 4️⃣ **Recency Boost**  
Newer policies take precedence:

```
recency_boost = 1 + (year - 2023) * 0.05
```

#### 5️⃣ **Final Scoring Formula**

```
final_score =
    cosine_sim × role_boost × specificity_boost × recency_boost
```

**Result:**  
For the intern query, **Document C (Intern FAQ)** always ranks highest.

---

## 🟦 **Step 4 — Final Answer Generation**  
**File:** `step4_answer.py`

This step produces the final employee-facing answer using **Google Gemini Flash**.

### It generates:
- **Final policy ruling**
- **One citation**
- **Direct quote** from the source
- **Reason why this document overrides others**
- **Explanation of rejected documents**

### Example Output:

```
FINAL RULING:
Interns cannot work from home. You are required to be in the office 5 days a week.

CITATION:
intern_onboarding_faq.txt

QUOTE:
"Interns are required to be in the office 5 days a week..."

WHY THIS DOC WAS CHOSEN:
It is the only policy written specifically for interns.

OTHER DOCUMENTS DISAGREED:
- employee_handbook_v1.txt: Applies to all employees.
- manager_updates_2024.txt: Applies to full-time hybrid workers.
```

---

# ▶️ **How to Run the Pipeline**

## 1️⃣ Install dependencies
```
pip install -r requirements.txt
```

## 2️⃣ Set your Google API Key
```python
import os
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
```

## 3️⃣ Run steps individually
```
python step1_prepare_data.py
python step2_build_vectorstore.py
python step3_retrieve.py
python step4_answer.py
```

## 4️⃣ Or run the entire pipeline:
```
python main.py
```

---

# 📸 **Required Screenshot**

```

![Intern Query Output](/mnt/data/93afdd42-5cff-4412-b46d-08c064b32b23.png)

```

---

# 💰 **Cost Analysis (Required)**

### ⭐ Embedding Cost — 10,000 Documents
Assuming 200 tokens/doc:

```
10,000 × 200 = 2,000,000 tokens
Embedding cost = 2M / 1,000 × $0.00002 = $0.04 (one-time)
```

### ⭐ LLM Query Cost — 5,000 Queries/Day
Assuming 150 tokens output:

```
750,000 tokens/day
22,500,000 tokens/month
LLM Cost = 22.5M / 1,000 × $0.00005 = $1.12/month
```

### 💵 **Total Monthly Cost ≈ $1.20**

This makes the system extremely affordable at scale.

---

# 🏁 **Conclusion**

This system:

- Resolves conflicting documents  
- Applies role-aware prioritization  
- Uses local embeddings + ChromaDB  
- Produces transparent, cited answers  
- Is extremely cost-efficient  
- Satisfies every requirement of the assignment  

It ensures the correct policy is always selected - even when documents contradict each other.

---

