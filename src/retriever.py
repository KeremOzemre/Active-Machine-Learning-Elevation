from dotenv import load_dotenv
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import googlemaps

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

# Google Elevation API allows up to 512 locations per request
_BATCH_SIZE = 512

# Shared client and thread pool
_client = googlemaps.Client(key=API_KEY)
_executor = ThreadPoolExecutor()


def _fetch_elevations_batch(points: list[tuple]) -> list[float]:
    """Fetch elevations for a batch of (lat, long) points using the official client."""
    results = _client.elevation(points)
    return [r["elevation"] for r in results]


async def request_elevation_area_async(
    start: tuple, end: tuple, samples: int
) -> dict[tuple, float]:
    """
    Asynchronously request elevations for evenly-spaced points between start and end.

    Denmark boundaries: lat: 54-58, long: 8-15

    start: (lat, long)
    end: (lat, long)
    samples: number of evenly-spaced samples along the path

    Returns a dict mapping each (lat, long) point to its elevation.
    """
    start_lat, start_long = start
    end_lat, end_long = end

    points = [
        (
            start_lat + (end_lat - start_lat) * i / (samples - 1),
            start_long + (end_long - start_long) * i / (samples - 1),
        )
        for i in range(samples)
    ]

    # Split into batches of up to _BATCH_SIZE and fire all batches concurrently
    batches = [points[i : i + _BATCH_SIZE] for i in range(0, len(points), _BATCH_SIZE)]

    loop = asyncio.get_running_loop()
    results = await asyncio.gather(
        *[loop.run_in_executor(_executor, _fetch_elevations_batch, batch) for batch in batches]
    )

    elevations = [elev for batch_result in results for elev in batch_result]
    return dict(zip(points, elevations))


def request_elevation_area(start: tuple, end: tuple, samples: int) -> dict[tuple, float]:
    """Synchronous wrapper around request_elevation_area_async."""
    return asyncio.run(request_elevation_area_async(start, end, samples))


async def request_elevation_async(lat: float, long: float) -> float:
    """Asynchronously request the elevation of a single (lat, long) point."""
    loop = asyncio.get_running_loop()
    elevations = await loop.run_in_executor(_executor, _fetch_elevations_batch, [(lat, long)])
    return elevations[0]


def request_elevation(lat: float, long: float) -> float:
    """Synchronous wrapper around request_elevation_async."""
    return asyncio.run(request_elevation_async(lat, long))


def save_data_file(start: tuple, end: tuple, samples: int, filename: str = "elevation_data.csv") -> None:
    """Save the elevation data to a CSV file."""
    path = Path(filename)
    data = request_elevation_area(start, end, samples)
    with path.open("w") as f:
        for (lat, long), elevation in data.items():
            f.write(f"{lat},{long},{elevation}\n")
