import os
import requests
from geopy.distance import geodesic
from models import Gym
from dotenv import load_dotenv

load_dotenv()

MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

if not MAPBOX_ACCESS_TOKEN:
    raise ValueError("MAPBOX_ACCESS_TOKEN is not set")

def search_gyms(longitude, latitude, limit, radius_km):

    url = "https://api.mapbox.com/search/searchbox/v1/forward"

    params = {
        "q": "gym",
        "proximity": f"{longitude},{latitude}",
        "limit": limit,
        "access_token": MAPBOX_ACCESS_TOKEN
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        return []

    data = response.json()

    gyms = []

    for feature in data.get("features", []):
        coords = feature["geometry"]["coordinates"]

        gym_lon = coords[0]
        gym_lat = coords[1]

        distance_km = geodesic(
            (latitude, longitude),
            (gym_lat, gym_lon)
        ).km

        # Filter gyms by distance
        if distance_km <= radius_km:
            gym = Gym(
                id=feature["properties"].get("mapbox_id", ""),
                name=feature["properties"].get("name", "Unknown"),
                latitude=gym_lat,
                longitude=gym_lon
            )

            gyms.append(gym)

    return gyms
    

