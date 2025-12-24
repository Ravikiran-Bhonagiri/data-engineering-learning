# Advance Project 32: AI Data Engineering (RAG Pipeline)

## 🎯 Goal
Master **Generative AI Infrastructure**. We will build the "Backend" of a RAG (Retrieval Augmented Generation) system: A pipeline that ingests text, chunks it, converts it into **Vector Embeddings**, and stores it in a mock Vector Database.

## 🛑 The "Context Window" Problem
*   **Scenario:** You want ChatGPT to answer questions about your private 1,000-page PDF manual.
*   **Problem:** You can't paste 1,000 pages into the prompt (Context Limit).
*   **Solution (RAG):**
    1.  **Ingest:** Chunk text into paragraphs.
    2.  **Embed:** Convert text to lists of numbers (Vectors) using a model (e.g., Titan/OpenAI).
    3.  **Store:** Put Vectors in a Database (OpenSearch/Pinecone).
    4.  **Retrieve:** When user asks question, find "nearest neighbor" vector and only send *that* paragraph to the LLM.

## 🛠️ The Solution: Embeddings
An embedding is a dense vector representation where semantically similar texts are close in mathematical space.
*   "Dog" is close to "Puppy".
*   "Dog" is far from "Carburator".

## 🏗️ Architecture
1.  **Source:** `raw_documents` (Text).
2.  **Unstructured ETL:** Chunking -> Embedding Model.
3.  **Sink:** Vector Store.

## 🚀 How to Run (Simulation)
1.  **Code:** `rag_pipeline.py`.
2.  **Result:** Observes text turning into high-dimensional arrays.
