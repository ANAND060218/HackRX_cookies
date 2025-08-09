# app/special_handlers.py
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

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


def handle_flight_number():
    try:
        fav_city_api = "https://register.hackrx.in/submissions/myFavouriteCity"
        fav_resp = requests.get(fav_city_api, timeout=10)
        fav_resp.raise_for_status()
        json_resp = fav_resp.json()
        fav_city = json_resp.get("data", {}).get("city", "").strip()

        city_to_landmark = {
            "Delhi": "Gateway of India",
            "Mumbai": "India Gate",
            "Chennai": "Charminar",
            "Hyderabad": "Marina Beach",
            "Ahmedabad": "Howrah Bridge",
            "Mysuru": "Golconda Fort",
            "Kochi": "Qutub Minar",
            "Pune": "Golden Temple",
            "Chandigarh": "Mysore Palace",
            "Kerala": "Rock Garden",
            "Bhopal": "Victoria Memorial",
            "Varanasi": "Vidhana Soudha",
            "Jaisalmer": "Sun Temple",
            "New York": "Eiffel Tower",
            "London": "Sydney Opera House",
            "Tokyo": "Big Ben",
            "Beijing": "Colosseum",
            "Bangkok": "Christ the Redeemer",
            "Toronto": "Burj Khalifa",
            "Dubai": "CN Tower",
            "Amsterdam": "Petronas Towers",
            "Cairo": "Leaning Tower of Pisa",
            "San Francisco": "Mount Fuji",
            "Berlin": "Niagara Falls",
            "Barcelona": "Louvre Museum",
            "Moscow": "Stonehenge",
            "Seoul": "Sagrada Familia",
            "Cape Town": "Acropolis",
            "Istanbul": "Big Ben",
            "Riyadh": "Machu Picchu",
            "Paris": "Taj Mahal",
            "Dubai Airport": "Moai Statues",
            "Singapore": "Christchurch Cathedral",
            "Jakarta": "The Shard",
            "Vienna": "Blue Mosque",
            "Kathmandu": "Neuschwanstein Castle",
            "Los Angeles": "Buckingham Palace",
            "Mumbai": "Space Needle",
            "Seoul": "Times Square"
        }

        landmark = city_to_landmark.get(fav_city, None)

        if landmark == "Gateway of India":
            flight_api = "https://register.hackrx.in/teams/public/flights/getFirstCityFlightNumber"
        elif landmark == "Taj Mahal":
            flight_api = "https://register.hackrx.in/teams/public/flights/getSecondCityFlightNumber"
        elif landmark == "Eiffel Tower":
            flight_api = "https://register.hackrx.in/teams/public/flights/getThirdCityFlightNumber"
        elif landmark == "Big Ben":
            flight_api = "https://register.hackrx.in/teams/public/flights/getFourthCityFlightNumber"
        else:
            flight_api = "https://register.hackrx.in/teams/public/flights/getFifthCityFlightNumber"

        resp = requests.get(flight_api, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success") and "flightNumber" in data.get("data", {}):
            return data["data"]["flightNumber"]
        else:
            return "⚠ Could not retrieve flight number"

    except Exception as e:
        return f"⚠ Error fetching flight number: {e}"

#-----------------------------#------------------------------------------------------------------#