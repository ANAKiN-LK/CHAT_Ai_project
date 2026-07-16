# Enterprise AI Chatbot with RAG

An enterprise-ready AI chatbot built with **FastAPI**, **LangGraph**, **Qdrant**, **vLLM**, and **Chainlit**. The system enables users to retrieve information from internal documents using Retrieval-Augmented Generation (RAG) while supporting local deployment through Docker.

---

## Overview

This project demonstrates how to build a production-style AI assistant capable of answering questions based on organizational documents instead of relying solely on the language model's internal knowledge.

The chatbot follows a Retrieval-Augmented Generation (RAG) workflow, allowing it to search relevant document chunks stored in Qdrant before generating responses with a locally hosted large language model.

The architecture is designed to be modular, making it suitable for experimentation, further development, and deployment in enterprise environments.

---

## Features

- Retrieval-Augmented Generation (RAG)
- LangGraph workflow for AI orchestration
- FastAPI backend
- Chainlit web interface
- Qdrant vector database
- HuggingFace Text Embedding Inference (TEI)
- Local LLM serving with vLLM
- Docker and Docker Compose support
- Streaming AI responses
- Modular project structure

---

## System Architecture

```
                User
                  │
                  ▼
          Chainlit Frontend
                  │
                  ▼
            FastAPI Backend
                  │
          LangGraph Workflow
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
     Qdrant Search      vLLM Server
          │                 │
          └────────┬────────┘
                   ▼
              Final Response
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language Model | vLLM |
| Embedding Model | HuggingFace TEI |
| Vector Database | Qdrant |
| AI Framework | LangGraph |
| Backend | FastAPI |
| Frontend | Chainlit |
| Containerization | Docker |
| Environment | Python |

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── graph/
│   │   ├── models/
│   │   ├── routers/
│   │   └── services/
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   ├── app.py
│   └── Dockerfile
│
├── scripts/
│   ├── ingestAll_to_qdrant.py
│   └── ingestpdf_to_qdrant.py
│
├── data/
├── docker-compose.yml
└── README.md
```

---

## Workflow

1. Documents are placed inside the **data** directory.
2. The ingestion script extracts document content.
3. Documents are split into semantic chunks.
4. Each chunk is converted into embeddings.
5. Embeddings are stored inside Qdrant.
6. User submits a question.
7. LangGraph retrieves the most relevant context.
8. The retrieved information is passed to the LLM.
9. The generated answer is streamed back to the user.

---

## Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/your-project.git

cd your-project
```

Install dependencies.

```bash
uv sync
```

Create an environment file.

```bash
cp .env.example .env
```

Configure your environment variables before running the application.

---

## Running the Project

### Step 1

Start the required services.

- Qdrant
- vLLM
- TEI

or simply use Docker Compose.

```bash
docker compose up --build
```

### Step 2

Ingest your documents.

```bash
uv run python scripts/ingest_all.py
```

### Step 3

Run the backend.

```bash
cd backend

uv run uvicorn app.main:app --reload
```

### Step 4

Run the frontend.

```bash
cd frontend

uv run chainlit run app.py
```

---
## Example Questions
```
What is the company's sick leave policy?
How can I request annual leave?
What employee benefits are available?
Where can I find the reimbursement policy?
```

---

## Future Improvements

- Conversation memory
- Authentication and authorization
- Multi-document collections
- Hybrid search
- Source citation highlighting
- Admin dashboard
- User management
- Conversation history
- Feedback collection

---

## License

This project is intended for educational  purposes.

---

## Author

**Tarakin Chobthamkit**
Institute of Field Robotics (FIBO)
King Mongkut's University of Technology Thonburi