from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

# CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect and fetch latest weather per city
def get_all_weather_data():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="weather",
        user="postgres",
        password="dhatri"
    )
    cur = conn.cursor()

    # ✅ Use the correct column name from your database: weather_condition
    cur.execute("""
        SELECT DISTINCT ON (city) city, temperature, humidity, weather_condition, timestamp
        FROM weather_data
        ORDER BY city, timestamp DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # ✅ Return 'description' key from 'weather_condition' column
    result = [
        {
            "city": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "description": row[3] or "--"
        }
        for row in rows
    ]
    return result

@app.get("/weather")
def read_all_weather():
    return get_all_weather_data()
