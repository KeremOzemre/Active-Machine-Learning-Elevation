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


def request_elevation_area(start, end, samples):
    """
    Request the elevation of a location using the Google Maps Elevation API.

    Denmark boundaries: lat: 54 58 - long: 8 15

    start: (lat, long)
    end: (lat, long)
    samples: number of samples to take in the area
    """

    start_lat = start[0]
    start_long = start[1]
    end_lat = end[0]
    end_long = end[1]

    # Points with equal distance between points
    points = []
    for i in range(samples):
        lat = start_lat + (end_lat - start_lat) * i / (samples - 1)
        long = start_long + (end_long - start_long) * i / (samples - 1)
        points.append((lat, long))

    # Request elevation for each point
    elevations = []
    for point in points:
        elevation = request_elevation(point[0], point[1])
        elevations.append(elevation)

    # Store elevations in dict with point as key
    elevations = {point: elevation for point, elevation in zip(points, elevations)}

    return elevations