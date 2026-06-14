
import pandas as pd
import random
import requests
import time
import os

from datetime import datetime
from dotenv import load_dotenv

load_dotenv("config/.env")

CHANNEL_ID = os.getenv("CHANNEL_ID")
READ_API_KEY = os.getenv("READ_API_KEY")

CSV_FILE = "data/air_quality_log.csv"

os.makedirs("data", exist_ok=True)


def classify_aqi(aqi):

    if aqi <= 100:
        return "GOOD"

    elif aqi <= 200:
        return "MODERATE"

    elif aqi <= 300:
        return "POOR"

    else:
        return "HAZARDOUS"


def upload_to_thingspeak(
    aqi,
    mq2,
    temperature,
    humidity,
    status
):

    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=100"

    payload = {

        "api_key": READ_API_KEY,
        "field1": aqi,
        "field2": mq2,
        "field3": temperature,
        "field4": humidity,
        "field5": status

    }

    try:

        response = requests.get(
            url,
            params=payload,
            timeout=10
        )

        print(
            "ThingSpeak Entry:",
            response.text
        )

    except Exception as e:

        print(
            "Upload Error:",
            e
        )


while True:

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    aqi = random.randint(50, 500)

    mq2 = random.randint(100, 1000)

    temperature = round(
        random.uniform(20, 40),
        1
    )

    humidity = round(
        random.uniform(30, 90),
        1
    )

    status = classify_aqi(aqi)

    alert = "NO"

    if status == "HAZARDOUS":
        alert = "YES"

    row = pd.DataFrame([{

        "Timestamp": timestamp,
        "AQI": aqi,
        "MQ2": mq2,
        "Temperature": temperature,
        "Humidity": humidity,
        "Status": status,
        "Alert": alert

    }])

    if os.path.exists(CSV_FILE):

        row.to_csv(
            CSV_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        row.to_csv(
            CSV_FILE,
            index=False
        )

    upload_to_thingspeak(
        aqi,
        mq2,
        temperature,
        humidity,
        status
    )

    print(row)

    time.sleep(16)