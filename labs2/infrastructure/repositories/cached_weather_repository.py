import time
from typing import Dict, Tuple

from labs2.domain.entities.weather_data import WeatherData
from labs2.domain.interfaces.weather_provider import WeatherProvider
from labs2.domain.interfaces.weather_repository import WeatherRepository


class CachedWeatherRepository(WeatherRepository):
    def __init__(self, provider: WeatherProvider, ttl_seconds: int = 60):
        self.provider = provider
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Tuple[WeatherData, float]] = {}

    def _is_valid(self, timestamp: float) -> bool:
        return (time.time() - timestamp) < self.ttl_seconds

    def get_weather(self, city: str) -> WeatherData:
        key = city.lower()
        if key in self._cache:
            data, ts = self._cache[key]
            if self._is_valid(ts):
                print("Using cached data")
                return data
        print("Fetching cached data")
        data = self.provider.fetch_weather(city)
        self._cache[key] = (data, time.time())
        return data
