import json
import time
import random
import datetime
from confluent_kafka import Producer

def generate_trade():
    """ Generates a random trade event with ISO timestamp. """
    return {
        "symbol": random.choice(["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]),
        "price": round(random.uniform(100.0, 1500.0), 2),
        "quantity": random.randint(1, 100),
        # Flink expects SQL standard timestamp format for JSON mapping
        "ts": datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')
    }

def main():
    conf = {'bootstrap.servers': 'localhost:9092'}
    producer = Producer(conf)
    topic = "trades"

    print("Sending trades to Flink... Press Ctrl+C to stop.")

    try:
        while True:
            trade = generate_trade()
            value = json.dumps(trade).encode('utf-8')
            producer.produce(topic, key=trade['symbol'], value=value)
            producer.poll(0)
            time.sleep(0.1)  # Fast generation

    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()

if __name__ == "__main__":
    main()
