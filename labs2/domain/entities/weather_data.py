from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherData:
    city: str
    temperature: float
    description: str

    feels_like: Optional[float] = None
    humidity: Optional[int] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_degree: Optional[int] = None
    wind_dir: Optional[str] = None
    cloud: Optional[int] = None
    uv_index: Optional[float] = None

    # Осадки
    precip_mm: Optional[float] = None
    rain_mm: Optional[float] = None
    snow_cm: Optional[float] = None

    # Время суток
    is_day: Optional[bool] = None
    sunrise: Optional[str] = None
    sunset: Optional[str] = None


