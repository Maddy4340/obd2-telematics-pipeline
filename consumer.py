import json
import psycopg2
from kafka import KafkaConsumer

conn = psycopg2.connect("host=localhost port=5432 dbname=telematics user=postgres password=password123")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_telemetry (
        time TIMESTAMPTZ NOT NULL,
        vehicle_id VARCHAR(50),
        speed FLOAT,
        rpm INT,
        coolant_temp FLOAT,
        engine_load FLOAT,
        throttle_pos FLOAT,
        is_anomaly BOOLEAN
    );
""")
conn.commit()

consumer = KafkaConsumer(
    'vehicle-stream',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Ingesting stream into TimescaleDB...")

for msg in consumer:
    d = msg.value
    anomaly_detected = d['coolant_temp'] > 102.0

    cursor.execute("""
        INSERT INTO vehicle_telemetry (time, vehicle_id, speed, rpm, coolant_temp, engine_load, throttle_pos, is_anomaly)
        VALUES (to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s)
    """, (d['timestamp'], d['vehicle_id'], d['speed'], d['rpm'], d['coolant_temp'], d['engine_load'], d['throttle_pos'], anomaly_detected))
    conn.commit()
    print(f"Saved: {d['vehicle_id']} | Anomaly: {anomaly_detected}")
