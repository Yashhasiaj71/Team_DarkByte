# AI-Based Stylometric Plagiarism Detection System

## 🚀 Project Overview
A full-stack web application prototype that detects AI-generated, paraphrased, and cross-language plagiarism using stylometric fingerprinting and semantic similarity analysis.

## 🎯 Features
- **Admin Panel**: Manage students, assignments, and view detailed reports.
- **Stylometric Fingerprinting**: Analyzes writing style (sentence length, vocabulary richness, etc.) to detect authorship anomalies.
- **AI Detection**: Estimates the probability of content being AI-generated.
- **Cross-Language Semantic Similarity**: Detects translated plagiarized content (simulated via TF-IDF).
- **Risk Scoring**: Aggregate risk score based on multiple metrics.

## 💻 Tech Stack
- **Backend**: Python (FastAPI), SQLAlchemy (SQLite), spaCy, scikit-learn.
- **Frontend**: React (Vite), Axios, Recharts, Lucide React (Icons).
- **OCR**: Tesseract (wrapper implemented).

## 📂 Structure
- `backend/`: FastAPI application and ML logic.
- `frontend/`: React admin dashboard.

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- Tesseract OCR (Optional, for image uploads)

### Quick Start (Windows)
1.  **Clone/Download** the repository.
2.  **Run Backend**: Double-click `run_backend.bat`.
    - This will install Python dependencies, seed the database with dummy data, and start the server at `http://localhost:8000`.
3.  **Run Frontend**: Double-click `run_frontend.bat`.
    - This will install Node dependencies and start the React app at `http://localhost:5173`.

### Manual Setup

#### Backend
```bash
cd backend
pip install -r requirements.txt
python seed_data.py  # Seed dummy data
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing the Prototype
1.  Open the Dashboard (`http://localhost:5173`).
2.  Navigate to **Upload Assignment**.
3.  Enter a **Student ID** (e.g., `1` for John, `2` for Alice).
4.  Enter an **Assignment ID** (e.g., `1`).
5.  Select a text file or enter text (currently file upload supported).
6.  Click **Upload & Analyze**.
7.  View the **Risk Report** with detailed metrics.

## 📊 Logic Explanation
- **Stylometry**: Extracts sentence length, type-token ratio, and POS distribution.
- **AI Detection**: Mock implementation returning a deterministic score based on text hash.
- **Similarity**: Calculates Cosine Similarity against all other submissions in the database.
- **Risk Score**: `(0.4 * Stylo) + (0.3 * AI) + (0.3 * Similarity)`.
