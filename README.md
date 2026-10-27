# obd2-telematics-pipeline
Real-time IoT vehicle telematics &amp; diagnostics pipeline using Kafka, TimescaleDB, Docker, and Streamlit
# Connected Vehicle Telematics & Diagnostics Pipeline

A real-time data engineering project that streams car sensor data (OBD-II), stores it in a time-series database, and shows live diagnostics on a web dashboard.

---

## What This Project Does
- Simulates real car sensor data (Speed, Engine RPM, Coolant Temperature).
- Uses **Apache Kafka** to stream data in real time.
- Stores historical trip data in **TimescaleDB (PostgreSQL)**.
- Flags engine overheating alerts.
- Displays live gauges and graphs using a **Streamlit** dashboard.

---

## Tech Stack Used
- **Python** (Core programming)
- **Apache Kafka** (Data streaming)
- **TimescaleDB / PostgreSQL** (Database)
- **Streamlit** (Live user interface)
- **Docker** (Running Kafka and Database)

---

## How to Run It on Your Machine

1. **Start the database and Kafka:**
   ```bash
   docker compose up -d
