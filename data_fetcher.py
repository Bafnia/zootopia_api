import requests
from dotenv import load_dotenv
import os

# lädt .env Datei
load_dotenv()

API_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv("API_KEY")  # holt den Key aus .env


def fetch_data(animal_name):
    """
    Fetches the animals data for the name 'animal_name'.
    """
    headers = {"X-Api-Key": API_KEY, "Accept": "application/json"}
    params = {"name": animal_name}

    response = requests.get(API_URL, headers=headers, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    return data if isinstance(data, list) else []
