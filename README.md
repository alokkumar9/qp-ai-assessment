# Contextual Chat Bot with Document Parsing

This project implements a simple contextual chat bot capable of reading and processing long PDF/Word documents using the Llama 3.2 3B model via Ollama.

[**MLOps PipeLine Link**](https://drive.google.com/file/d/1a0ja1J-z4G-qmMd2qXrG0NWKFg5D4jLl/view?usp=drive_link "MLOps Pipeline Draw")

**Ollama to run LLama3.2 3B Model Locally**

## Embedding Model

This project uses the HuggingFace embedding model:

- Model: **BAAI/bge-large-en-v1.5**
- Implementation: **HuggingFaceEmbeddings**

## Setup

### Install NVIDIA Driver and CUDA Toolkit

```bash
sudo apt install nvidia-driver-535
sudo apt install nvidia-cuda-toolkit
```

Verify installation:
```bash
nvidia-smi
nvcc --version
```

## GPU Management

List available GPUs:
```bash
nvidia-smi -L
```

## GPU Selector Script

 GPU selector script, run and select the GPU:
```bash
chmod +x ollama_gpu_selector.sh
sudo ./ollama_gpu_selector.sh
```

### Ollama Service Management

Start Ollama:
```bash
sudo systemctl start ollama
```

Check Ollama status:
```bash
sudo systemctl status ollama
```

Disable automatic start:
```bash
sudo systemctl disable ollama
```

One can stop Ollama if not required:
```bash
sudo systemctl stop ollama
```

## Ollama Model Management

Run Llama 3.2:
```bash
ollama run llama3.2
```

List all models:
```bash
ollama ls
```

Remove a model:
```bash
ollama rm <model_name>
```

Stop a specific model:
```bash
ollama stop <model_name>
```
---
**This project implements a FastAPI-based system for uploading documents, generating embeddings, and querying the uploaded content.**

## Installation
To set up the project, follow these steps:

1. Clone the repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Install uvicorn (if not included in requirements.txt):

```bash
pip install uvicorn
```

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn app:app --reload
```

This will start the server with hot-reloading enabled for development purposes.

## API Endpoints

The application provides two main endpoints:

### 1. Upload Endpoint

- **URL**: `/upload/`
- **Method**: POST
- **Description**: Upload a document file to the system.
- **Response**: Returns a secret key for querying the uploaded document.

### 2. Query Endpoint

- **URL**: `/query/`
- **Method**: POST
- **Description**: Query the uploaded document using the secret key.
- **Request Body**:
  - `secret`: The secret key received from the upload endpoint
  - `query`: The question to ask about the document

## Troubleshooting

If port 8000 is engaged:
```bash
sudo lsof -t -i tcp:8000 | xargs kill -9
```

# RAG Performance Evaluation using Giskard

This instructions on how to perform performance evaluation of a Retrieval-Augmented Generation (RAG) system using Giskard, specifically focusing on the RAGET (RAG Evaluation Toolkit) feature.

## Overview

Giskard is an open-source Python library that offers tools for testing, monitoring, and evaluating machine learning and AI models, including RAG systems. RAGET, a component of Giskard, allows for comprehensive evaluation of RAG systems by automatically generating test sets and assessing various components of the RAG pipeline.

## Prerequisites

1. Install Giskard:
   ```bash
   pip install giskard
   ```

2. Ensure you have your RAG system implemented and ready for evaluation.

## Steps for RAG Evaluation

### 1. Generate Test Set

RAGET can automatically generate a test set from your RAG system's knowledge base. This test set includes:

- `question`: The generated question
- `reference_context`: The context that can be used to answer the question
- `reference_answer`: The answer to the question (generated with LLM)

### 2. Prepare Your RAG Agent

Wrap your RAG agent in a function that takes a question as input and returns an answer:

```python
def get_answer_fn(question: str, history=None) -> str:
    # Your RAG agent implementation here
    return answer
```

### 3. Run the Evaluation

Use the `giskard.rag.evaluate` function to evaluate your RAG agent:

```python
from giskard.rag import evaluate

report = evaluate(get_answer_fn, testset=testset, knowledge_base=knowledge_base)
```

### 4. Analyze the Results

RAGET computes scores for each component of the RAG agent:

- **Generator**: The LLM used inside the RAG to generate answers
- **Retriever**: Fetches relevant documents from the knowledge base
- **Rewriter**: Rewrites user queries for relevance or to account for chat history
- **Router**: Filters user queries based on intentions
- **Knowledge Base**: The set of documents given to the RAG

Each component is scored on a scale from 0 to 100, with 100 being a perfect score.

### 5. One can Include Additional Metrics (Optional)

We can include additional RAGAS metrics in your evaluation:

```python
from giskard.rag.metrics.ragas_metrics import ragas_context_recall, ragas_faithfulness

report = evaluate(
    get_answer_fn,
    testset=testset,
    knowledge_base=knowledge_base,
    metrics=[ragas_context_recall, ragas_faithfulness]
)
```


