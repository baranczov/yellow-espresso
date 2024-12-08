import json
import sys
import os

import requests

sys.path.append(os.getcwd())
from config import API_KEY


def get_location(location):
    try:
        response = requests.get(
            "https://dataservice.accuweather.com"
            "/locations/v1/cities/translate.json",
            params={
                "apikey": API_KEY,
                "q": location.lower(),
                "language": "ru-ru",
                "details": "true",
            },
        )
        response.raise_for_status()

        data = response.json()
        if data:
            return (data[0]["Key"], data[0]["LocalizedName"])
        else:
            return None  # Если данные пустые

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении местоположения: {e}")
        return None


def get_weather_by_location(location_key):
    try:
        response = requests.get(
            "https://dataservice.accuweather.com"
            f"/forecasts/v1/daily/1day/{location_key}",
            params={
                "apikey": API_KEY,
                "language": "ru-ru",
                "details": "true",
                "metric": "true",
            },
        )
        response.raise_for_status()

        data = response.json()
        temperature = data["DailyForecasts"][0]["Temperature"]["Maximum"][
            "Value"
        ]
        humidity = data["DailyForecasts"][0]["Day"]["RelativeHumidity"][
            "Average"
        ]
        wind_speed = data["DailyForecasts"][0]["Day"]["Wind"]["Speed"]["Value"]
        rain_probability = data["DailyForecasts"][0]["Day"]["RainProbability"]

        weather_data = {
            "temperature": ("Температура (°C)", temperature),
            "humidity": ("Влажность (%)", humidity),
            "wind_speed": ("Скорость ветра (км/ч)", wind_speed),
            "rain_prob": ("Вероятность дождя (%)", rain_probability),
        }

        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении погоды: {e}")
        return None


def main():
    location_key, localized_name = get_location("Москва")
    if location_key:
        data = get_weather_by_location(location_key)

        print(f"Погода в городе {localized_name}:\n")
        endlen = max(map(lambda x: len(x[0]), data.values())) + 3
        answer = ""
        for name, value in data.values():
            answer += f"{name}{' ' * (endlen - len(name))}| {value}\n"
        print(answer, end="")

        with open("weather_data.json", "w") as file:
            json.dump(data, file)


if __name__ == "__main__":
    main()
