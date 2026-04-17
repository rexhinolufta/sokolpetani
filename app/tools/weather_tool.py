import httpx
from config.settings import settings


async def get_weather(city: str) -> dict:
    url = f"{settings.weather_api}/{city}?format=j1"
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    current = data.get("current_condition", [{}])[0]
    return {
        "city": city,
        "temp_c": current.get("temp_C"),
        "feels_like_c": current.get("FeelsLikeC"),
        "humidity": current.get("humidity"),
        "weather_desc": (
            current.get("weatherDesc", [{}])[0].get("value")
            if current.get("weatherDesc")
            else None
        ),
    }
