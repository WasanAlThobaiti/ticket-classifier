Markdown
# 🚀 Enterprise-Grade AI Ticket Classifier

An asynchronous, production-ready AI ticket classification engine built with **FastAPI**, **SQLAlchemy**, and an automated background worker system. Designed for high-throughput operational environments, this system automatically ingests, analyzes, and categorizes incoming support tickets with precision.

---

## ✨ Key Features & Architecture

- **Asynchronous Processing Engine**: Uses background workers to handle ticket classification tasks seamlessly without blocking API responses.
- **Robust Database Layer**: Powered by SQLite & SQLAlchemy with automated schema management and startup seeding.
- **Enterprise Endpoints**: 
  - Automated sample ticket ingestion and storage.
  - Full CRUD operations for ticket tracking and retrieval.
  - Dedicated **Re-classification Endpoint** (`/tickets/{id}/reclassify`) to re-queue tickets for processing.
- **Graceful Lifecycle Management**: Implements modern FastAPI `lifespan` handlers for clean startup routines and safe in-flight task completion upon shutdown.
- **Custom Dark & Gorgeous Swagger UI**: A tailored, visually stunning dark mode theme built directly into the interactive API documentation.
- **Evaluation Framework**: Built-in evaluation scripts to measure system performance and accuracy.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **Database**: SQLite, SQLAlchemy ORM, Pydantic v2
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest

---

## ⚙️ Getting Started & Installation

### Running Locally with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone [https://github.com/WasanAlThobaiti/ticket-classifier.git](https://github.com/WasanAlThobaiti/ticket-classifier.git)
   cd ticket-classifier
Build and run the container using Docker Compose:

Bash
docker compose up --build -d
Access the interactive API documentation (Custom Dark Theme):

Plaintext
http://localhost:8000/docs
🧪 Running Tests
To verify the test suite and ensure all components are functioning correctly:

Bash
docker compose exec ticket-classifier pytest
📊 Evaluation
To run the system evaluation script:

Bash
python evaluate.py