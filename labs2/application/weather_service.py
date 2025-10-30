from labs2.domain.interfaces.weather_repository import WeatherRepository


class WeatherService:
    def __init__(self, repository: WeatherRepository):
        self.repository = repository

    def get_weather_summary(self, city: str) -> str:
        w = self.repository.get_weather(city)

        lines = [f"🌆 Погода в {w.city}: {w.temperature:.1f}°C, {w.description}"]

        optional_fields = {
            "feels_like": ("🌡️ Ощущается как", lambda v: f"{v:.1f}°C"),
            "humidity": ("💧 Влажность", lambda v: f"{v}%"),
            "pressure": ("📈 Давление", lambda v: f"{v} мбар"),
            "wind_speed": ("🌬️ Ветер", lambda v: f"{v} м/с" + (f" ({w.wind_dir})" if w.wind_dir else "")),
            "cloud": ("☁️ Облачность", lambda v: f"{v}%"),
            "uv_index": ("🌞 UV-индекс", str),
            "precip_mm": ("🌧️ Осадки", lambda v: f"{v} мм"),
            "rain_mm": ("🌧️ Дождь", lambda v: f"{v} мм"),
            "snow_cm": ("❄️ Снег", lambda v: f"{v} см"),
        }

        for attr, (label, fmt) in optional_fields.items():
            value = getattr(w, attr, None)
            if value is not None:
                lines.append(f"{label}: {fmt(value)}")

        if w.is_day is not None:
            lines.append("🌞 День" if w.is_day else "🌙 Ночь")

        if w.sunrise and w.sunset:
            lines.append(f"🌅 Восход: {w.sunrise}, 🌇 Закат: {w.sunset}")

        return "\n".join(lines)
