import json
from confluent_kafka import Consumer, KafkaError

def main():
    # 1. Configuration
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'python-consumer-group-1',
        'auto.offset.reset': 'earliest' # Start from beginning if no offset stored
    }

    # 2. Create Consumer
    consumer = Consumer(conf)
    
    # 3. Subscribe to Topic
    consumer.subscribe(['trades'])

    print("Starting Consumer... Press Ctrl+C to stop.")

    try:
        while True:
            # 4. Poll for new messages (timeout 1.0s)
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    continue

            # 5. Process Message
            try:
                data = json.loads(msg.value().decode('utf-8'))
                print(f"Received Trade: {data['symbol']} @ ${data['price']} (Qty: {data['quantity']})")
            except Exception as e:
                print(f"Error parsing message: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        # 6. Clean Shutdown
        consumer.close()

if __name__ == "__main__":
    main()
