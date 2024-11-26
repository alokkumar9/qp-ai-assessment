# Contextual Chat Bot with Document Parsing

This project implements a simple contextual chat bot capable of reading and processing long PDF/Word documents using the Llama 3.2 3B model via Ollama.

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

