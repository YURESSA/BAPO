import requests
from labs2.domain.entities.weather_data import WeatherData
from labs2.domain.interfaces.weather_provider import WeatherProvider


class WeatherAPIProvider(WeatherProvider):
    BASE_URL = "http://api.weatherapi.com/v1/current.json"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_weather(self, city: str) -> WeatherData:
        params = {
            "key": self.api_key,
            "q": city,
            "lang": "ru",
        }
        resp = requests.get(self.BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        current = data.get("current", {})
        condition = current.get("condition", {})
        location = data.get("location", {})

        is_day = bool(current.get("is_day", 1))

        wind_speed = current.get("wind_kph")
        wind_degree = current.get("wind_degree")
        wind_dir = current.get("wind_dir")

        return WeatherData(
            city=location.get("name", city),
            temperature=current.get("temp_c"),
            feels_like=current.get("feelslike_c"),
            humidity=current.get("humidity"),
            pressure=current.get("pressure_mb"),
            wind_speed=wind_speed,
            wind_degree=wind_degree,
            wind_dir=wind_dir,
            cloud=current.get("cloud"),
            uv_index=current.get("uv"),
            description=condition.get("text", ""),
            precip_mm=current.get("precip_mm"),
            rain_mm=current.get("precip_mm") if current.get("precip_mm", 0) > 0 else None,
            snow_cm=current.get("snow_cm") if current.get("snow_cm", 0) > 0 else None,
            is_day=is_day,
            sunrise=None,
            sunset=None
        )
