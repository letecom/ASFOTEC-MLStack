#!/usr/bin/env python
import os
import sys
import json
from confluent_kafka import Consumer, KafkaError
import psycopg2
from contextlib import contextmanager
from datetime import datetime

KAFKA_TOPIC = 'predictions'
POSTGRES_DSN = os.getenv('POSTGRES_DSN', 'postgresql://postgres:postgres@postgres:5432/predictions_log')

@contextmanager
def get_pg_conn():
    conn = psycopg2.connect(POSTGRES_DSN)
    try:
        yield conn
    finally:
        conn.close()

def create_table_if_not_exists():
    with get_pg_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS predictions_log (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                prediction INTEGER,
                proba FLOAT,
                model_version TEXT,
                latency_ms FLOAT,
                features_json TEXT
            );
        """)
        conn.commit()
        cur.close()

def main():
    create_table_if_not_exists()
    
    conf = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'redpanda:9092'),
        'group.id': 'prediction-logger',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([KAFKA_TOPIC])
    
    print(f'Consuming from {KAFKA_TOPIC} → Postgres...')
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f'Error: {msg.error()}')
                    break
            
            event = json.loads(msg.value().decode('utf-8'))
            # Anonymize features if needed (e.g., remove PII keys)
            features_json = json.dumps(event.get('features', {}))
            
            with get_pg_conn() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO predictions_log (timestamp, prediction, proba, model_version, latency_ms, features_json)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    datetime.fromisoformat(event['timestamp']),
                    event['prediction'],
                    event['proba'],
                    event['model_version'],
                    event['latency_ms'],
                    features_json
                ))
                conn.commit()
                cur.close()
            
            print(f'Logged prediction {event["prediction"]} (proba={event["proba"]:.2f})')
            
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    main()
