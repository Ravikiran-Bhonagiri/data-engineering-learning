import json
import time
import random
from confluent_kafka import Producer

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def generate_trade():
    """ Generates a random trade event. """
    return {
        "symbol": random.choice(["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]),
        "price": round(random.uniform(100.0, 1500.0), 2),
        "quantity": random.randint(1, 100),
        "timestamp": int(time.time() * 1000)
    }

def main():
    # 1. Configuration
    conf = {'bootstrap.servers': 'localhost:9092'}
    
    # 2. Create Producer
    producer = Producer(conf)
    topic = "trades"

    print("Starting Producer... Press Ctrl+C to stop.")

    try:
        while True:
            # 3. Serialize Data
            trade = generate_trade()
            value = json.dumps(trade).encode('utf-8')
            
            # 4. Send Data (Asynchronous)
            # The 'key' ensures trades for the same symbol go to the same partition
            producer.produce(topic, key=trade['symbol'], value=value, callback=delivery_report)
            
            # Trigger any available delivery report callbacks from previous produce() calls
            producer.poll(0)
            
            time.sleep(0.5) 

    except KeyboardInterrupt:
        pass
    finally:
        # 5. Flush (Wait for outstanding messages to be delivered)
        producer.flush()

if __name__ == "__main__":
    main()
