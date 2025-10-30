import requests
from labs2.domain.entities.weather_data import WeatherData
from labs2.domain.interfaces.weather_provider import WeatherProvider


class WeatherStackProvider(WeatherProvider):
    BASE_URL = "http://api.weatherstack.com/current"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_weather(self, city: str) -> WeatherData:
        params = {
            "access_key": self.api_key,
            "query": city,
            "units": "m",
        }
        resp = requests.get(self.BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        current = data.get("current", {})
        location = data.get("location", {})

        wind_speed = current.get("wind_speed")
        wind_degree = current.get("wind_degree")
        wind_dir = current.get("wind_dir")

        precip_mm = current.get("precip")
        rain_mm = precip_mm if precip_mm and precip_mm > 0 else None
        snow_cm = None

        return WeatherData(
            city=location.get("name", city),
            temperature=current.get("temperature"),
            feels_like=current.get("feelslike"),
            humidity=current.get("humidity"),
            pressure=current.get("pressure"),
            wind_speed=wind_speed,
            wind_degree=wind_degree,
            wind_dir=wind_dir,
            cloud=current.get("cloudcover"),
            uv_index=current.get("uv_index"),
            description=current.get("weather_descriptions")[0] if current.get("weather_descriptions") else "",
            precip_mm=precip_mm,
            rain_mm=rain_mm,
            snow_cm=snow_cm,
            is_day=bool(current.get("is_day") == "yes"),
            sunrise=None,
            sunset=None
        )
