import os
import json
import requests
import time
from kafka import KafkaProducer
from dotenv import load_dotenv
from cities import cities  # Your original list of 50 cities

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please check your .env file.")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

while True:
    for city in cities:
        try:
            weather_data = fetch_weather(city)
            city_name = city.split(",")[0]

            # ✅ Safe fallback if description not available
            description = (
                weather_data["weather"][0]["description"]
                if "weather" in weather_data and weather_data["weather"]
                else "Not Available"
            )

            cleaned_data = {
                "city": city_name,
                "temperature": weather_data["main"]["temp"],
                "humidity": weather_data["main"]["humidity"],
                "description": description
            }

            producer.send('weather-data', value=cleaned_data)
            print(f"✅ Sent weather data for {city_name}")
            print(json.dumps(cleaned_data, indent=2))

        except Exception as e:
            print(f"❌ Failed for {city}: {e}")

    time.sleep(10)
