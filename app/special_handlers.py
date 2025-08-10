# app/special_handlers.py
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from app.processor import extract_text_from_url
from app.llm_reasoner import generate_batch_answer
from langchain.docstore.document import Document
#-----------------------------#------------------------------------------------------------------#
def handle_secret_token(doc_url: str):
    try:
        resp = requests.get(doc_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        token_div = soup.find("div", {"id": "token"})
        token_value = token_div.get_text(strip=True) if token_div else "⚠ Token not found"
        return token_value
    except Exception as e:
        return f"⚠ Error fetching token: {e}"
# app/special_handlers.py

def handle_flight_number():
    try:
        # Step 1: Get favourite city
        fav_city_api = "https://register.hackrx.in/submissions/myFavouriteCity"
        fav_resp = requests.get(fav_city_api, timeout=10)
        fav_resp.raise_for_status()
        fav_city = fav_resp.json().get("data", {}).get("city", "").strip()

        if not fav_city:
            return "⚠ Could not retrieve favourite city"

        # Step 2: Extract PDF text using your existing function
        pdf_url = (
            "https://hackrx.blob.core.windows.net/hackrx/rounds/"
            "FinalRound4SubmissionPDF.pdf?sv=2023-01-03&spr=https&"
            "st=2025-08-07T14%3A23%3A48Z&se=2027-08-08T14%3A23%3A00Z&"
            "sr=b&sp=r&sig=nMtZ2x9aBvz%2FPjRWboEOZIGB%2FaGfNf5TfBOrhGqSv4M%3D"
        )
        pdf_text, ext = extract_text_from_url(pdf_url)
        if not pdf_text or not ext:
            return f"⚠ Failed to read PDF: {pdf_text}"

        # Step 3: Prompt LLM to return only the URL
        llm_question = (
            f"The favourite city is '{fav_city}'. From the provided PDF content, "
            "find the single correct URL associated with that city to retrieve the flight number. "
            "Respond with ONLY the exact URL, nothing else."
        )

        context_docs = [Document(page_content=pdf_text)]
        llm_answer = generate_batch_answer([context_docs], [llm_question])[0].strip()

        if not llm_answer.startswith("http"):
            return f"⚠ LLM did not return a valid URL: {llm_answer}"

        # Step 4: Hit the URL and get flight number
        flight_resp = requests.get(llm_answer, timeout=10)
        flight_resp.raise_for_status()
        data = flight_resp.json()

        if data.get("success") and "flightNumber" in data.get("data", {}):
            return data["data"]["flightNumber"]

        return "⚠ Could not retrieve flight number"

    except Exception as e:
        return f"⚠ Error fetching flight number: {e}"
