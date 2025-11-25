import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyDyDgw3qPdwbcznE8KIAdvPT-n5rYC0InM"

%%writefile step4_answer.py
"""
STEP 4 — Final Answer using Gemini 2.0 Flash (Kaggle-Compatible)
"""

import os
import google.generativeai as genai

# -----------------------------------------
# Load API key
# -----------------------------------------
if "GOOGLE_API_KEY" not in os.environ:
    raise EnvironmentError("GOOGLE_API_KEY is missing.")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# -----------------------------------------
# Prompt builder
# -----------------------------------------
def build_prompt(query, user_role, ranked_docs):
    context = ""
    for i, d in enumerate(ranked_docs, start=1):
        context += (
            f"\nDocument {i} — {d['metadata']['source']}\n"
            "---------------------------------------\n"
            f"{d['text']}\n"
        )

    return f"""
You are NebulaGears' internal policy assistant.

User query:
\"{query}\"

User role:
{user_role}

Retrieved documents:
{context}

Your tasks:
1. Give the final ruling for THIS user role.
2. Cite ONLY one document.
3. Provide ONE short quote.
4. Briefly explain why other documents do not apply.
5. Follow strictly:

FINAL RULING:
<answer>

CITATION:
<filename>

QUOTE:
"<quote>"

WHY THIS DOC WAS CHOSEN:
<reason>

OTHER DOCUMENTS DISAGREED:
<list>
"""


# -----------------------------------------
# CALL GEMINI 2.0 FLASH  (THIS WORKS)
# -----------------------------------------
def call_gemini(prompt):
    model = genai.GenerativeModel("models/gemini-2.0-flash")  # <--- WORKS IN YOUR LIST
    response = model.generate_content(prompt)
    return response.text


# -----------------------------------------
# Final answer
# -----------------------------------------
def generate_answer(query, user_role, ranked_docs):
    prompt = build_prompt(query, user_role, ranked_docs)
    output = call_gemini(prompt)

    print("\n----- FINAL ANSWER -----\n")
    print(output)
    return output


# -----------------------------------------
# Test execution
# -----------------------------------------
if __name__ == "__main__":
    from step3_retrieve import retrieve_docs
    
    ranked = retrieve_docs(
        query="I just joined as a new intern. Can I work from home?",
        user_role="intern"
    )

    generate_answer(
        query="I just joined as a new intern. Can I work from home?",
        user_role="intern",
        ranked_docs=ranked
    )

!python step4_answer.py
