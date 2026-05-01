
import requests
from app.config import OLLAMA_URL, MODEL_NAME


def generate_answer(query, context_chunks):

    context = "\n".join(context_chunks)

    prompt = f"""
    You are a helpful assistant.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        print("OLLAMA RESPONSE:", data)

        return data.get("response", "No response generated")

    except Exception as e:
        return f"Error generating answer: {str(e)}"