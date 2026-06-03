# Hotel-rag-bot — Grounded Hotel Concierge AI (FAISS + Gemini)

Welcome to the **Aurelius Concierge Hotel Chatbot**, an intelligent, RAG-powered (Retrieval-Augmented Generation) virtual concierge designed for modern hotels. It leverages FAISS for fast vector similarity search and Google's Gemini API for highly contextual and grounded responses.

## 🌟 Key Features

- **Context-Aware Responses:** Answers guest queries accurately based on your specific hotel policies, amenities, and room information using RAG.
- **Multilingual Support:** Seamlessly detects and responds in English, Hindi, and Hinglish.
- **Intent Classification:** Automatically categorizes guest queries (e.g., Room Service, Booking, Policy, Greeting) to provide structured handling.
- **Strict Guardrails:** Prevents hallucination by triggering a graceful fallback if the answer is not found in the provided knowledge base (e.g., "I couldn't find that information. Let me connect you with a representative.").
- **Admin Dashboard:** A built-in UI for hotel staff to monitor total queries, average retrieval scores, hallucination rates, and guest satisfaction.
- **Feedback Loop:** Guests can rate responses, allowing continuous improvement.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, SQLite
- **AI/ML:** Google Gemini API (LLM), Sentence-Transformers (`all-MiniLM-L6-v2` for embeddings), FAISS (Vector Database)
- **Frontend:** React, Vite, Tailwind CSS
- **Containerization:** Docker & Docker Compose

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+ (for local frontend development)
- Docker (optional, for containerized deployment)
- A Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

### 1. Clone the Repository

```bash
git clone https://github.com/Aryanpatil963/Hotel-rag-bot-Grounded-Hotel-Concierge-AI-FAISS-Gemini-.git
cd Hotel-rag-bot-Grounded-Hotel-Concierge-AI-FAISS-Gemini-
```

### 2. Environment Variables

Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY="your_api_key_here"
```

### 3. Run with Docker (Recommended)

The easiest way to run the entire application is using Docker Compose:

```bash
docker-compose up --build
```
- The **Frontend** will be available at: `http://localhost:3000`
- The **Backend API** will be available at: `http://localhost:8000`

### 4. Run Manually (Local Development)

#### Backend Setup
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the React development server
npm run dev
```

## 📚 Knowledge Base Ingestion

The chatbot reads from documents stored in the `data/` folder (e.g., `amenities.txt`, `hotel_policies.pdf`, `room_info.json`).
To update the knowledge base, add your files to the `data/` directory and trigger the ingestion pipeline:

```bash
curl -X POST http://localhost:8000/api/ingest
```
This will parse the new documents, generate embeddings, and update the local FAISS vector index.

## 📊 Admin Dashboard

Access the Admin Dashboard via the frontend UI by clicking the "Admin Dashboard" button. It provides real-time statistics stored in the local SQLite database (`conversations.db`).

## 🛡️ License
This project is open-source and available under the [MIT License](LICENSE).
