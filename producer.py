import json
import random
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Streaming vehicle telemetry to Kafka topic 'vehicle-stream'...")

while True:
    is_anomaly = random.random() < 0.05
    coolant_temp = random.uniform(105, 120) if is_anomaly else random.uniform(85, 95)

    payload = {
        "timestamp": time.time(),
        "vehicle_id": "MH-14-EV-2026",
        "speed": round(random.uniform(40, 90), 2),
        "rpm": int(random.uniform(1800, 3200)),
        "coolant_temp": round(coolant_temp, 2),
        "engine_load": round(random.uniform(20, 65), 2),
        "throttle_pos": round(random.uniform(15, 45), 2)
    }

    producer.send('vehicle-stream', payload)
    print(f"Sent: RPM={payload['rpm']} | Temp={payload['coolant_temp']}C")
    time.sleep(1)
