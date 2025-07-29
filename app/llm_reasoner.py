import os
from openai import OpenAI
from langchain_core.documents import Document
from dotenv import load_dotenv  # ✅ Load environment variables

# ✅ Load .env variables
load_dotenv()

# ✅ Set the Groq-compatible OpenAI client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("api_key")  # ✅ Load key from .env
)

# ✅ Set the model name
GROQ_MODEL = "llama3-70b-8192"

def generate_answer(contexts: list[Document], question: str) -> str:
    try:
        context_text = "\n\n".join(doc.page_content for doc in contexts)

        prompt = f"""You are a helpful assistant.
Answer the question based on the following context.

Context:
{context_text}

Question: {question}
Answer:"""

        print("\n\n--- PROMPT SENT TO GROQ ---")
        print("--- END PROMPT ---\n\n")

        # 🧠 Chat completion using new client
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq error:", e)
        return "❌ Error generating response from Groq"
