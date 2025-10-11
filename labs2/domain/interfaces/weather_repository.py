from abc import ABC, abstractmethod

from labs2.domain.entities.weather_data import WeatherData


class WeatherRepository(ABC):
    @abstractmethod
    def get_weather(self, city: str) -> WeatherData:
        """Возвращает WeatherData (возможно из кэша)"""
        raise NotImplementedError