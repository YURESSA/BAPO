from labs2.domain.interfaces.weather_ui import WeatherUI


class ConsoleUI(WeatherUI):
    def run(self):
        print("=== Weather App ===")
        try:
            while True:
                city = input("Введите город (или 'exit'): ").strip()
                if not city or city.lower() in ("exit", "quit"):
                    print("Выход.")
                    break

                try:
                    summary = self.service.get_weather_summary(city)
                    print(summary)
                except Exception as e:
                    print(f"Ошибка при получении погоды: {e}")
        except KeyboardInterrupt:
            print("\nПользователь прервал выполнение.")
