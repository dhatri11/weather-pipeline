import os
import json
import requests
import time
from kafka import KafkaProducer
from dotenv import load_dotenv
from cities import cities

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please check your .env file.")

# Corrected serializer: use json.dumps instead of json.dump
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
            producer.send('weather-data', value=weather_data)
            print(f" Sent weather data for {city}")
            print(json.dumps(weather_data, indent=2))  # Optional: view the data
        except Exception as e:
            print(f" Failed for {city}: {e}")
    time.sleep(10)
