import os
from enum import Enum

from dotenv import load_dotenv

from application.weather_service import WeatherService
from infrastructure.providers.fake_provider import FakeWeatherProvider
from infrastructure.repositories.cached_weather_repository import CachedWeatherRepository
from labs2.infrastructure.providers.weatherapi_provider import WeatherAPIProvider
from labs2.infrastructure.providers.weatherstack_provider import WeatherStackProvider
from labs2.presentation.qt_ui import WeatherApp
from presentation.console_ui import ConsoleUI

PROVIDERS_CONFIG = {
    "weatherapi": {
        "env": "WEATHERAPI_KEY",
        "cls": WeatherAPIProvider,
        "emoji": "🌦️",
    },
    "weatherstack": {
        "env": "WEATHERSTACK_API_KEY",
        "cls": WeatherStackProvider,
        "emoji": "🌤️",
    },
}


class WeatherProviderEnum(str, Enum):
    WEATHERAPI = "weatherapi"
    WEATHERSTACK = "weatherstack"


class UIEnum(Enum):
    QT = ("qt", WeatherApp)
    CONSOLE = ("console", ConsoleUI)

    def __init__(self, label, ui_class):
        self.label = label
        self.ui_class = ui_class


def build_app(provider_name: WeatherProviderEnum = WeatherProviderEnum.WEATHERAPI,
              ui_type: UIEnum = UIEnum.CONSOLE,
              use_fake: bool = False):
    load_dotenv()

    if use_fake:
        provider = FakeWeatherProvider()
    else:
        config = PROVIDERS_CONFIG.get(provider_name.value)
        if not config:
            raise ValueError(f"Unknown provider_name: {provider_name.value}")

        api_key = os.getenv(config["env"])
        if not api_key:
            raise RuntimeError(f"{config['env']} not set in environment. See .env.example")

        provider = config["cls"](api_key=api_key)

    repository = CachedWeatherRepository(provider=provider, ttl_seconds=120)
    service = WeatherService(repository=repository)

    ui_class = ui_type.ui_class
    return ui_class(service=service)


if __name__ == "__main__":
    ui = build_app(
        provider_name=WeatherProviderEnum.WEATHERSTACK,
        ui_type=UIEnum.CONSOLE,
        use_fake=False
    )
    ui.run()
