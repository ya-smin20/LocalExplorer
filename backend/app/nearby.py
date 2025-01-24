import os
from dotenv import load_dotenv
import requests
from typing import List, Dict

load_dotenv()



FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")

def fetch_nearby_places(lat: float, lon: float) -> List[Dict]:
    """Fetch nearby places using the Foursquare API."""
    url = f"https://api.foursquare.com/v3/places/nearby"
    params = {
        "ll": f"{lat},{lon}",  
        "radius": 1000,  
        "limit": 20,  
    }
    
    headers = {
        "Authorization": FOURSQUARE_API_KEY,
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        places = []
        for place in data.get("results", []):
            name = place.get("name")
            lat = place.get("geocodes", {}).get("main", {}).get("latitude")
            lon = place.get("geocodes", {}).get("main", {}).get("longitude")
            
            if name and lat and lon:
                places.append({"name": name, "latitude": lat, "longitude": lon})
        
        return places
    except requests.RequestException as e:
        print(f"Error fetching nearby places: {e}")
        return []

def generate_map_url(name: str, latitude: float, longitude: float):
  
    return f"https://www.google.com/maps?q={latitude},{longitude}({name})"
