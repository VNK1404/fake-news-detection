# Multi-Modal Fake News Detection Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![License](https://img.shields.io/badge/License-MIT-green)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

An AI-powered, production-ready platform built to assess the authenticity of digital claims. It processes documents (PDFs and images), extracts key claims, and runs them through simultaneous local and remote verification pipelines — all backed by a Python/Flask API and a Next.js/TypeScript frontend.

---

## 📑 Table of Contents

- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Architecture & Pipeline Flow](#️-architecture--pipeline-flow)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📂 Project Structure

This repository follows a monorepo layout that houses both the backend and frontend components together:

* **[`backend/`](backend/README.md)**: Python/Flask API service responsible for OCR-based document scanning, claim extraction, and orchestrating the parallel verification engine.
* **[`frontend/verinews-ui/`](frontend/verinews-ui/README.md)**: Next.js + TypeScript + Tailwind CSS web dashboard displaying interactive real-time analysis reports and analytics charts.

---

## ⚡ Key Features

* **Multi-Modal Document Processing**: Upload scanned documents, PDFs, or images.
* **Optical Character Recognition (OCR)**: Leverages Tesseract OCR to scan documents and extract readable text.
* **Semantic Claim Extraction**: Automatically extracts the core claim from raw text using AI.
* **Parallel Asynchronous Verification**:
  1. **Local Fine-Tuned RoBERTa Classifier**: Fine-tuned model yielding `99.96%` validation F1-score.
  2. **FAISS Semantic Similarity Search**: Low-latency matching against **44,898** news claims using `all-MiniLM-L6-v2` dense embeddings.
  3. **Google Fact Check API**: Real-time cross-referencing with global fact-checking databases.
  4. **NewsAPI Search**: Real-time validation against news sources.
  5. **The Guardian Content API**: Validation against trusted news publications.
* **Weighted Decision Engine**: Combines all model outputs and API responses to deliver a unified final verdict (`Real`, `Fake`, or `Uncertain`) along with an associated confidence score.
* **Premium Dashboard UI**: Responsive interface featuring glassmorphic design and real-time step progress visualization.

---

## 📊 Model Performance

Our fine-tuned **RoBERTa** model was benchmarked against a curated fake news dataset, achieving the following results:

| Metric | Score |
|--------|-------|
| **Validation F1-Score** | 99.96% |
| **Validation Accuracy** | 99.95% |
| **Training Dataset Size** | ~44,898 news claims |
| **Embedding Model** | `all-MiniLM-L6-v2` |
| **Vector Index** | FAISS (IndexFlatL2) |

> The FAISS similarity index enables sub-millisecond semantic matching at scale.

---

## ⚙️ Architecture & Pipeline Flow

```mermaid
graph TD
    A[Scanned Document / Image / PDF] --> B[Tesseract OCR / PDF Parser]
    B --> C[Text Cleaner & Validator]
    C --> D[Claim Extractor]
    D --> E{Parallel Worker Pool}
    E --> F[RoBERTa Classifier]
    E --> G[FAISS Similarity Search]
    E --> H[Google Fact Check API]
    E --> I[NewsAPI]
    E --> J[The Guardian API]
    F & G & H & I & J --> K[Response Normalizer]
    K --> L[Weighted Decision Engine]
    L --> M[Consensus Verdict + Confidence]
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Python 3.10+, Flask |
| **AI / ML** | RoBERTa (fine-tuned), Hugging Face Transformers |
| **Vector Search** | FAISS + `all-MiniLM-L6-v2` embeddings |
| **OCR** | Tesseract OCR, PyMuPDF |
| **External APIs** | Google Fact Check, NewsAPI, The Guardian API |
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS |
| **LLM Integration** | Google Gemini API |

---

## 🚀 Getting Started

Use the instructions below to get both the backend and frontend up and running on your local machine:

### 1. Backend Setup
1. Change directory to `backend`:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables (e.g. in `.env`):
   ```bash
   GEMINI_API_KEY="your-gemini-key"
   GOOGLE_API_KEY="your-google-api-key"
   NEWS_API_KEY="your-news-api-key"
   GUARDIAN_API_KEY="your-guardian-api-key"
   ```
4. Build the local FAISS semantic similarity search index:
   ```bash
   python -m fake_news_module.similarity.index_builder
   ```
5. Run the Flask development server:
   ```bash
   python app.py
   ```
   The API will start running on [http://localhost:5000](http://localhost:5000).

### 2. Frontend Setup
1. Change directory to `frontend/verinews-ui`:
   ```bash
   cd frontend/verinews-ui
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

---

## 🔐 Environment Variables

Store all API keys in a `.env` file within the `backend/` directory. Make sure you never commit this file to version control.

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | Google Gemini API key for claim extraction |
| `GOOGLE_API_KEY` | ✅ Yes | Google Fact Check Tools API key |
| `NEWS_API_KEY` | ✅ Yes | NewsAPI.org key for real-time news validation |
| `GUARDIAN_API_KEY` | ✅ Yes | The Guardian Open Platform API key |
| `FLASK_ENV` | ⬜ Optional | Set to `development` for debug mode |

> 💡 Copy `.env.example` to `.env` and fill in your credentials before running the backend.

---

## 🔌 API Endpoints

The Flask backend exposes the following REST API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/scan` | Upload a PDF/image document for full analysis |
| `POST` | `/api/verify-text` | Directly verify a raw text claim |
| `GET` | `/api/health` | Health check — returns service status |
| `GET` | `/api/history` | Retrieve past verification results |

> **Base URL (local):** `http://localhost:5000`

---

## 🤝 Contributing

We warmly welcome contributions! To get started, please follow the steps outlined below:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 🖼️ Screenshots & Demo

> The platform ships with a high-end glassmorphic dashboard that delivers live, step-by-step progress updates throughout the verification process.

| Feature | Description |
|---------|-------------|
| 📤 Document Upload | Drag-and-drop PDF / image uploader |
| 🔍 Live Analysis | Animated step-by-step verification pipeline |
| 📈 Confidence Score | Color-coded verdict with percentage confidence |
| 📊 Analytics Charts | Historical trends and verdict distribution |
| 🌙 Dark Mode | Full dark-mode glassmorphic UI |

> 💡 **Live Demo**: Clone the repo and run both backend and frontend locally to experience the full platform.

---

## 🙏 Acknowledgements

- [Hugging Face Transformers](https://huggingface.co/transformers/) — RoBERTa model hosting and fine-tuning
- [FAISS by Facebook AI Research](https://github.com/facebookresearch/faiss) — Efficient similarity search
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — Open-source OCR engine
- [Google Fact Check Tools API](https://developers.google.com/fact-check/tools/api/) — Fact-checking database
- [NewsAPI](https://newsapi.org/) — Real-time news aggregation
- [The Guardian Open Platform](https://open-platform.theguardian.com/) — Trusted journalism API

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
