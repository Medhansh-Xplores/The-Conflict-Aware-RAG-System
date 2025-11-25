%%writefile step1_prepare_data.py
import json
import re

# -----------------------------------------
# Clean the text lightly
# -----------------------------------------
def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------------------
# Simple chunking (small docs → 1 chunk each)
# -----------------------------------------
def chunk_text(text, max_chars=600):
    text = clean_text(text)
    if len(text) <= max_chars:
        return [text]
    # fallback for future large docs
    return [text[:max_chars], text[max_chars:]]


# -----------------------------------------
# Create prepared_docs.jsonl
# -----------------------------------------
def prepare_step1():

    documents = [
        {
            "fname": "employee_handbook_v1.txt",
            "text": """At NebulaGears, we believe in complete freedom. All employees are eligible for the 'Work From Anywhere' program. You can work remotely 100% of the time from any location. No prior approval is needed.""",
            "roles": "employee,all_employees",
            "type": "policy",
            "date": "2023-01-01"
        },
        {
            "fname": "manager_updates_2024.txt",
            "text": """Update to remote work policy: Effective immediately, remote work is capped at 3 days per week. Employees must be in the HQ office on Tuesdays and Thursdays. All remote days require manager approval.""",
            "roles": "employee,manager",
            "type": "update",
            "date": "2024-06-01"
        },
        {
            "fname": "intern_onboarding_faq.txt",
            "text": """Welcome to the team! Please note that while full-time employees have hybrid options, interns are required to be in the office 5 days a week for the duration of their internship to maximize mentorship. No remote work is permitted for interns.""",
            "roles": "intern",
            "type": "faq",
            "date": "2024-01-01"
        }
    ]

    output = []

    for d in documents:
        chunks = chunk_text(d["text"])
        for i, chunk in enumerate(chunks):
            output.append({
                "id": f"{d['fname']}::chunk{i+1}",
                "source": d["fname"],
                "text": chunk,
                "metadata": {
                    "source": d["fname"],
                    "applicable_roles": d["roles"],  # string for Chroma
                    "type": d["type"],
                    "date": d["date"]
                }
            })

    # Write JSONL file
    with open("prepared_docs.jsonl", "w", encoding="utf-8") as f:
        for item in output:
            f.write(json.dumps(item) + "\n")

    print(f"✔ created prepared_docs.jsonl with {len(output)} chunks")


if __name__ == "__main__":
    prepare_step1()

!python step1_prepare_data.py
