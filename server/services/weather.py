import httpx
from typing import Dict, Any, Optional

async def get_live_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Fetches real-time weather & rain forecast from Open-Meteo API.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m&hourly=precipitation_probability,precipitation&forecast_days=1"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                return {
                    "source": "open-meteo",
                    "latitude": latitude,
                    "longitude": longitude,
                    "temperature_c": current.get("temperature_2m"),
                    "humidity_percent": current.get("relative_humidity_2m"),
                    "precipitation_mm": current.get("precipitation", 0.0),
                    "rain_mm": current.get("rain", 0.0),
                    "wind_speed_kmh": current.get("wind_speed_10m"),
                    "weather_code": current.get("weather_code")
                }
    except Exception as e:
        print(f"Weather API fetch failed: {e}")

    # Fallback default if offline/network issue
    return {
        "source": "simulated_radar",
        "latitude": latitude,
        "longitude": longitude,
        "temperature_c": 28.5,
        "humidity_percent": 82,
        "precipitation_mm": 18.5,
        "rain_mm": 18.5,
        "wind_speed_kmh": 22.0,
        "weather_code": 63  # Moderate rain
    }
