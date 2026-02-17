from dotenv import load_dotenv
import os
load_dotenv()

import requests

API_KEY = os.getenv("GOOGLE_API_KEY")

def request_location(lat, long) -> dict:
    """Request the elevation of a location using the Google Maps Elevation API."""

    response = requests.get(
        f"https://maps.googleapis.com/maps/api/elevation/json?"
        f"locations={lat},{long}"
        f"&key={API_KEY}",
    )

    return response.json()

def request_elevation(lat, long):
    """Request the elevation of a location using the Google Maps Elevation API."""

    response = request_location(lat, long)

    if response["status"] == "OK":
        return response["results"][0]["elevation"]
    else:
        raise Exception(f"Error requesting elevation: {response['status']}")



