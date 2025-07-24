import json
import psycopg2
from kafka import KafkaConsumer

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="weather",     #  Your database name in pgAdmin
    user="postgres",      #  Your pgAdmin username (default is 'postgres')
    password="dhatri",  #  Replace this with your actual password
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Create table if it doesn’t exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city VARCHAR(50),
        temperature FLOAT,
        humidity INT,
        weather_condition VARCHAR(50),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Kafka consumer
consumer = KafkaConsumer(
    'weather-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(" Waiting for weather data from Kafka...")

for message in consumer:
    data = message.value
    try:
        city = data.get('name')
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        condition = data['weather'][0]['main']

        cursor.execute("""
            INSERT INTO weather_data (city, temperature, humidity, weather_condition)
            VALUES (%s, %s, %s, %s)
        """, (city, temp, humidity, condition))
        conn.commit()
        print(f" Inserted data for {city}")

    except Exception as e:
        print(f" Failed to insert: {e}")
