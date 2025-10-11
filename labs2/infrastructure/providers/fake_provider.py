from labs2.domain.entities.weather_data import WeatherData
from labs2.domain.interfaces.weather_provider import WeatherProvider


class FakeWeatherProvider(WeatherProvider):
    """Простой фейковый провайдер для тестов и демонстрации"""

    def fetch_weather(self, city: str) -> WeatherData:
        return WeatherData(
            city=city,
            temperature=20.5,
            feels_like=20.0,
            humidity=50,
            pressure=1013.0,
            wind_speed=5.0,
            wind_degree=180,
            wind_dir="S",
            cloud=20,
            uv_index=3.5,
            precip_mm=0.0,
            rain_mm=0.0,
            snow_cm=0.0,
            is_day=True,
            sunrise="06:30",
            sunset="19:45",
            description="Ясно (fake)"
        )
