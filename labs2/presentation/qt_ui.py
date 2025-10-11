import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from labs2.domain.interfaces.weather_ui import WeatherUI


class DummyService:
    def get_weather_summary(self, city):
        return f"Погода в {city}: 🌞"


class WeatherQtUI(QWidget):
    """Qt-представление приложения погоды"""
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weather App 🌦️")
        layout = QVBoxLayout()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Введите город")
        layout.addWidget(self.city_input)

        get_btn = QPushButton("Получить погоду")
        get_btn.clicked.connect(self.show_weather)
        layout.addWidget(get_btn)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def show_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.result_area.setText("Введите название города")
            return
        try:
            summary = self.service.get_weather_summary(city)
            self.result_area.setText(summary)
        except Exception as e:
            self.result_area.setText(f"Ошибка: {e}")


class WeatherApp(WeatherUI):
    """Главный класс для запуска UI через интерфейс WeatherUI"""
    def run(self):
        app = QApplication(sys.argv)
        ui = WeatherQtUI(self.service)
        ui.show()
        sys.exit(app.exec())

