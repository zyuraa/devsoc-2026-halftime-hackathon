import os
import requests
from geopy.distance import geodesic
from models import Gym
from dotenv import load_dotenv

load_dotenv()

MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

if not MAPBOX_ACCESS_TOKEN:
    raise ValueError("MAPBOX_ACCESS_TOKEN is not set")


def search_gyms(longitude, latitude, limit=10, radius_km=5):
    """
    Searches for gyms near a given coordinate using the Mapbox Search Box API.

    Parameters:
        longitude (float): Longitude of the search centre.
            Example: 131.2433

        latitude (float): Latitude of the search centre.
            Example: -23.8438

        limit (int, optional): Maximum number of results to request from Mapbox, capped at 10.

        radius_km (float, optional): Maximum distance from the given coordinate,
            in kilometres.

    Returns:
        list[Gym]: A list of Gym objects within radius_km of the given coordinate.
    """

    url = "https://api.mapbox.com/search/searchbox/v1/forward"

    params = {
        "q": "gym",
        "proximity": f"{longitude},{latitude}",
        "limit": min(limit, 10),
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
                longitude=gym_lon,
                groups=[]
            )

            gyms.append(gym)

    return gyms
    
# if __name__ == "__main__":
#     gyms = search_gyms(
#         longitude=151,
#         latitude=-34,
#         limit=10,
#         radius_km=15
#     )

#     for gym in gyms:
#         print(gym.id, gym.name, gym.latitude, gym.longitude)
