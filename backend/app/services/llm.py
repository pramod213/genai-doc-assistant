



import requests


def generate_answer(question, context):
    prompt = f"""
You are a strict document-based AI assistant.

You MUST follow these rules:

RULES:
- Return answer ONLY in bullet points.
- Do not return paragraphs.
- Do not include context text.
- Answer ONLY using the given context.
- Do NOT use outside knowledge.
- If the answer is not in the context, reply EXACTLY:
- "I don't know based on the document. Please ask questions related to the document."
- Always respond in short, clear bullet points.
- Keep answers concise and to the point.

---------------------
CONTEXT:
{context}
---------------------

QUESTION:
{question}

ANSWER:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1
            }
        )

        response.raise_for_status()

        result = response.json()

        return result.get("response", "").strip()

    except Exception as e:
        return "I don't know based on the document. Please ask questions related to the document."