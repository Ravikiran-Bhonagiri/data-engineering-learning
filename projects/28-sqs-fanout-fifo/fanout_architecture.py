import json
import uuid

# Mocking the Architecture Flow in Python
# In AWS, these are separate services.

class MockSNS:
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, queue):
        self.subscribers.append(queue)
        
    def publish(self, message, group_id=None):
        print(f"[SNS Topic] Received: {message['event']} (Group: {group_id})")
        print(f"   -> Fanning out to {len(self.subscribers)} queues...")
        for queue in self.subscribers:
            queue.send_message(message, group_id)

class MockSQS:
    def __init__(self, name, is_fifo=False):
        self.name = name
        self.is_fifo = is_fifo
        self.queue = []
        
    def send_message(self, message, group_id=None):
        # FIFO Logic simulation
        if self.is_fifo and not group_id:
             print(f"      [ERROR] {self.name} is FIFO but missing MessageGroupId!")
             return

        self.queue.append(message)
        print(f"      -> [{self.name}] Enqueued message.")

def main():
    # 1. Setup Infrastructure
    sns_topic = MockSNS()
    
    # Queue 1: Billing (Needs Strict Ordering -> FIFO)
    billing_queue = MockSQS("BillingQueue.fifo", is_fifo=True)
    
    # Queue 2: Analytics (Standard, just needs the data)
    analytics_queue = MockSQS("AnalyticsQueue", is_fifo=False)
    
    # 2. Wire Subscription (Fan-Out)
    sns_topic.subscribe(billing_queue)
    sns_topic.subscribe(analytics_queue)
    
    # 3. Simulate Traffic (Financial Transactions)
    user_id = "User_A" # This acts as MessageGroupId for FIFO
    
    print("\n--- Transaction 1: Account Created ---")
    sns_topic.publish({"event": "ACCOUNT_CREATED", "amt": 0}, group_id=user_id)
    
    print("\n--- Transaction 2: Deposit $100 ---")
    sns_topic.publish({"event": "DEPOSIT", "amt": 100}, group_id=user_id)
    
    print("\n--- Transaction 3: Buy Item $50 ---")
    sns_topic.publish({"event": "PURCHASE", "amt": 50}, group_id=user_id)
    
    # 4. Verify FIFO State
    print("\n--- Verifying Billing Queue (FIFO) ---")
    print(f"Queue Depth: {len(billing_queue.queue)}")
    print("Expected Order: Created -> Deposit -> Purchase")
    # In a real FIFO queue, this order is guaranteed even if multiple consumers are reading.

if __name__ == "__main__":
    main()
