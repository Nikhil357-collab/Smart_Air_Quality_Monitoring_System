import streamlit as st
import pandas as pd
import requests
import os

from dotenv import load_dotenv

load_dotenv("config/.env")

CHANNEL_ID = os.getenv("CHANNEL_ID")
READ_API_KEY = os.getenv("READ_API_KEY")

st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

st.title(
    "🌍 IoT Air Quality Monitoring Dashboard"
)

url = (
    f"https://api.thingspeak.com/channels/"
    f"{CHANNEL_ID}/feeds.json"
    f"?api_key={READ_API_KEY}"
    f"&results=50"
)

try:

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()
    
    feeds = data["feeds"]

    df = pd.DataFrame(feeds)

    if len(df) == 0:

        st.warning(
            "No Data Available"
        )

    else:

        df["field1"] = pd.to_numeric(
            df["field1"]
        )

        df["field2"] = pd.to_numeric(
            df["field2"]
        )

        df["field3"] = pd.to_numeric(
            df["field3"]
        )

        df["field4"] = pd.to_numeric(
            df["field4"]
        )

        latest = df.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "AQI",
            int(latest["field1"])
        )

        col2.metric(
            "MQ2",
            int(latest["field2"])
        )

        col3.metric(
            "Temperature",
            latest["field3"]
        )

        col4.metric(
            "Humidity",
            latest["field4"]
        )

        st.divider()

        st.subheader(
            "AQI Trend"
        )

        st.line_chart(
            df["field1"]
        )

        st.subheader(
            "MQ2 Trend"
        )

        st.line_chart(
            df["field2"]
        )

        st.subheader(
            "Temperature Trend"
        )

        st.line_chart(
            df["field3"]
        )

        st.subheader(
            "Humidity Trend"
        )

        st.line_chart(
            df["field4"]
        )

        latest_aqi = int(
            latest["field1"]
        )

        if latest_aqi > 300:

            st.error(
                "🚨 Hazardous Air Quality"
            )

        elif latest_aqi > 200:

            st.warning(
                "⚠ Poor Air Quality"
            )

        else:

            st.success(
                "✅ Air Quality Acceptable"
            )

        st.subheader(
            "Raw ThingSpeak Data"
        )

        st.dataframe(
            df.tail(20),
            use_container_width=True
        )

except Exception as e:

    st.error(
        f"Connection Error: {e}"
    )