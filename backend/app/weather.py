import os
from dotenv import load_dotenv
import requests
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)

load_dotenv()


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def fetch_weather(lat: float, lon: float):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        logger.error("Weather API Key is missing!")
        raise HTTPException(status_code=500, detail="Weather API Key is missing")

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    logger.info(f"Fetching weather data for coordinates: lat={lat}, lon={lon}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Weather data fetched successfully: {response.json()}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching weather data")
