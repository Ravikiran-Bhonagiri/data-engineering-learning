# Advanced Project 26: Step Functions (Distributed Map)

## 🎯 Goal
Master **Serverless Parallelism**. We will design a State Machine that uses the **Distributed Map** state to process thousands of S3 objects concurrently, a pattern that replaces complex Spark jobs for many file processing use cases.

## 🛑 The "Loop" Problem
*   **Standard Map:** Loops through a JSON array (limited to 40 items).
*   **Problem:** If you have 100,000 CSV files in S3 to parse, a standard loop times out or hits payload limits.
*   **Solution:** **Distributed Map**. You pass an S3 Bucket as input. Step Functions spawns 10,000 concurrent "Child Workflow" executions to process the files.

## 🛠️ The Solution: ItemReader (S3)
The `Map` state is configured with an `ItemReader`.
1.  **Reader:** List Objects V2 (S3).
2.  **Processor:** Lambda Function (`process_file`).
3.  **Concurrency:** Adaptive (up to 10,000).

## 🏗️ Architecture
1.  **Input:** S3 Bucket (`my-landing-zone`).
2.  **Map State:** Iterates over keys in the bucket.
3.  **Item Processor:** Lambda that reads *one* file and processes it.

## 🚀 How to Run (Simulation)
1.  **Definition:** `map_workflow.asl.json`.
2.  **Lambda:** `file_processor.py`.
3.  **Note:** This is a High-Scale pattern. In the AWS Console, you would see thousands of green "Success" dots in the Map Run visualization.
