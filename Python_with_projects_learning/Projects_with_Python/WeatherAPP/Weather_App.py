
import requests
import subprocess
import json

# Windows voice function
def speak(text):
    safe_text = json.dumps(str(text))

    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$s.Rate = 0; "
        f"$s.Speak({safe_text}); "
        "$s.Dispose()"
    )

    subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True
    )


def get_weather(city):
    # Step 1: Search for the city in Nepal
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 10,
        "language": "en",
        "countryCode": "NP"
    }

    geo_response = requests.get(
        geo_url, params=geo_params, timeout=15
    )
    geo_response.raise_for_status()

    geo_data = geo_response.json()
    results = geo_data.get("results", [])

    if not results:
        speak("Sorry, this city or town was not found in Nepal.")
        return

    # Prefer an exact name match when available
    location = next(
        (place for place in results
         if place["name"].casefold() == city.casefold()),
        results[0]
    )

    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]
    country = location.get("country", "Nepal")

    print(f"\nWeather for {city_name}, {country}")
    speak(f"Getting the weather for {city_name}, Nepal.")

    # Step 2: Get current weather for the selected location
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,precipitation,wind_speed_10m"
        ),
        "timezone": "auto"
    }

    response = requests.get(
        weather_url, params=weather_params, timeout=15
    )
    response.raise_for_status()

    data = response.json()
    weather = data["current"]

    # Step 3: Display and speak every detail
    temperature = weather["temperature_2m"]
    humidity = weather["relative_humidity_2m"]
    feels_like = weather["apparent_temperature"]
    wind_speed = weather["wind_speed_10m"]
    precipitation = weather["precipitation"]

    print("Temperature:", temperature, "°C")
    speak(f"Temperature is {temperature} degrees Celsius.")

    print("Humidity:", humidity, "%")
    speak(f"Humidity is {humidity} percent.")

    print("Feels like:", feels_like, "°C")
    speak(f"Feels like temperature is {feels_like} degrees Celsius.")

    print("Wind speed:", wind_speed, "km/h")
    speak(f"Wind speed is {wind_speed} kilometers per hour.")

    print("Precipitation:", precipitation, "mm")
    speak(f"Precipitation is {precipitation} millimeters.")


# Main program
speak("Welcome to the Nepal Weather App.")

while True:
    city = input(
        "\nEnter a city or town in Nepal "
        "(or type exit to quit): "
    ).strip()

    if city.casefold() == "exit":
        speak("Goodbye. Thank you for using the Nepal Weather App.")
        break

    if not city:
        print("Please enter a city name.")
        continue

    try:
        get_weather(city)

    except requests.RequestException:
        print("Unable to connect to the weather service.")
        speak("Unable to connect to the weather service.")

    except (KeyError, ValueError):
        print("Unable to read the weather data.")
        speak("Unable to read the weather data.")

    except subprocess.CalledProcessError:
        print("Windows speech engine failed.")
        break








