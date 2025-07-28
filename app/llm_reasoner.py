import os
import google.generativeai as genai
from langchain_core.documents import Document

# ✅ Load the Gemini API key from environment FIRST
GEMINI_API_KEY = "AIzaSyAhzeZhr9QTUHtDUDuvEoOMex13RV9jXDg"

genai.configure(api_key=GEMINI_API_KEY)  # ✅ Now this works

# ✅ Load the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")
print("Loaded GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))


def generate_answer(contexts: list[Document], question: str) -> str:
    try:
        context_text = "\n\n".join(doc.page_content for doc in contexts)

        prompt = f"""You are a helpful assistant.
Answer the question based on the following context.

Context:
{context_text}

Question: {question}
Answer:"""

        print("\n\n--- PROMPT SENT TO GEMINI ---")
        print(prompt)
        print("--- END PROMPT ---\n\n")

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return "❌ Error generating response from Gemini"
