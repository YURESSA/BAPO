from abc import ABC, abstractmethod


class WeatherUI(ABC):
    """Абстрактный интерфейс для любых UI"""

    def __init__(self, service):
        self.service = service

    @abstractmethod
    def run(self):
        pass