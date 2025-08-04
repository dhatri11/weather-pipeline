import json
import psycopg2
from kafka import KafkaConsumer

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="weather",
    user="postgres",
    password="dhatri",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table if not exists
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

print("⏳ Waiting for weather data from Kafka...")

for message in consumer:
    data = message.value
    try:
        city = data['city']
        temp = data['temperature']
        humidity = data['humidity']
        condition = data.get('description', '--') or '--'

        cursor.execute("""
            INSERT INTO weather_data (city, temperature, humidity, weather_condition)
            VALUES (%s, %s, %s, %s)
        """, (city, temp, humidity, condition))
        conn.commit()
        print(f"✅ Inserted data for {city}: {condition}")

    except Exception as e:
        print(f"❌ Failed to insert: {e}")
