from abc import ABC, abstractmethod

from labs2.domain.entities.weather_data import WeatherData


class WeatherProvider(ABC):
    @abstractmethod
    def fetch_weather(self, city: str) -> WeatherData:
        """Запрашивает погоду у конкретного провайдера и возвращает WeatherData"""
        raise NotImplementedError
