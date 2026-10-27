import streamlit as st
import pandas as pd
import psycopg2
import time

st.set_page_config(page_title="Telematics Live Dashboard", layout="wide")
st.title("Connected Vehicle Telematics & Diagnostics")

def get_data():
    conn = psycopg2.connect("host=localhost port=5432 dbname=telematics user=postgres password=password123")
    df = pd.read_sql("SELECT * FROM vehicle_telemetry ORDER BY time DESC LIMIT 50", conn)
    conn.close()
    return df

placeholder = st.empty()

while True:
    try:
        df = get_data()
        if not df.empty:
            with placeholder.container():
                latest = df.iloc[0]
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Current Speed", f"{latest['speed']} km/h")
                col2.metric("Engine RPM", f"{latest['rpm']}")
                col3.metric("Coolant Temp", f"{latest['coolant_temp']} °C")
                col4.metric("Status", "ALERT: Overheat" if latest['is_anomaly'] else "Normal")

                st.subheader("Live Telemetry History")
                st.line_chart(df.set_index('time')[['rpm', 'coolant_temp']])
    except Exception as e:
        st.write("Waiting for data to stream...")
    time.sleep(2)
