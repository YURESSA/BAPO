import os
from enum import Enum
from dotenv import load_dotenv

from application.weather_service import WeatherService
from infrastructure.providers.fake_provider import FakeWeatherProvider
from labs2.infrastructure.providers.weatherapi_provider import WeatherAPIProvider
from labs2.infrastructure.providers.weatherstack_provider import WeatherStackProvider
from infrastructure.repositories.cached_weather_repository import CachedWeatherRepository
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


WeatherProviderEnum = Enum("WeatherProviderEnum", {k.upper(): k for k in PROVIDERS_CONFIG.keys()})


def build_app(provider_name: WeatherProviderEnum = WeatherProviderEnum.WEATHERAPI, use_fake: bool = False):
    load_dotenv()

    if use_fake:
        provider = FakeWeatherProvider()
    else:
        provider_key = provider_name.value
        config = PROVIDERS_CONFIG.get(provider_key)
        if not config:
            raise ValueError(f"Unknown provider_name: {provider_key}")

        api_key = os.getenv(config["env"])
        if not api_key:
            raise RuntimeError(f"{config['env']} not set in environment. See .env.example")

        provider = config["cls"](api_key=api_key)

    repository = CachedWeatherRepository(provider=provider, ttl_seconds=120)
    service = WeatherService(repository=repository)
    ui = ConsoleUI(service=service)
    return ui


if __name__ == "__main__":
    ui = build_app(provider_name=WeatherProviderEnum.WEATHERSTACK)
    ui.run()
