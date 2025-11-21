# MediSense-AI
# 🏥 MediSense AI - Unified Medical Report Summarizer & Symptom Checker

[![Angular](https://img.shields.io/badge/Angular-17-red)](https://angular.io/)
[![Flask](https://img.shields.io/badge/Flask-3.0-blue)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> **Empowering patients with AI-driven medical insights through intelligent report analysis and symptom checking**

MediSense AI is a GenAI-powered healthcare assistant that bridges the gap between complex medical documentation and patient understanding. Using advanced OCR, LLM, and RAG technologies, it transforms medical reports into comprehensible summaries and provides evidence-based symptom analysis.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Dataset & RAG Pipeline](#-dataset--rag-pipeline)
- [Team](#-team)
- [Deployment](#-deployment-100-free-for-hackathon)
- [Demo](#-demo)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔍 Medical Report Summarizer
- **Multi-format Support**: Upload PDF or image-based medical reports
- **Advanced OCR**: Automated text extraction using Tesseract/EasyOCR
- **Dual Summaries**: 
  - Patient-friendly explanations in simple language
  - Doctor-focused technical summaries
- **Key Insights**:
  - Primary diagnosis identification
  - Medication list with dosages
  - Test results and interpretations
  - Critical warnings and alerts
  - Follow-up recommendations

### 🩺 AI-Powered Symptom Checker
- **RAG-Based Analysis**: Retrieves information from verified medical knowledge bases (WHO/NIH)
- **Intelligent Insights**:
  - Possible conditions and differential diagnosis
  - Medical reasoning and explanations
  - Urgency classification (Low/Medium/High)
  - Source citations from medical literature
- **Context-Aware**: Considers multiple symptoms for accurate analysis

### 📊 Interactive Dashboard
- Unified upload panel for medical documents
- Real-time summary display with formatting
- Intuitive symptom input interface
- Medical history tracking (optional)
- Responsive design for mobile and desktop

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Angular Frontend (UI)                     │
│          (Upload, Display, Symptom Input, Dashboard)         │
└────────────────────────┬────────────────────────────────────┘
                         │ REST APIs (HTTP/JSON)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Flask Backend (API)                      │
│              (Route Handling, Business Logic)                │
└────────────┬───────────────────────┬────────────────────────┘
             │                       │
             ▼                       ▼
┌────────────────────────┐  ┌──────────────────────────────┐
│   OCR Processing       │  │   AI Processing Layer        │
│   (Tesseract/EasyOCR)  │  │   - LLM Service (Gemini/GPT) │
└────────────────────────┘  │   - RAG Service              │
                            │   - Prompt Engineering        │
                            └──────────┬───────────────────┘
                                       │
                                       ▼
                            ┌──────────────────────────────┐
                            │   Knowledge Base (RAG)       │
                            │   - ChromaDB/FAISS           │
                            │   - Medical Embeddings       │
                            │   - WHO/NIH Dataset          │
                            └──────────────────────────────┘
```

### Data Flow

**Medical Report Processing:**
```
User Upload → OCR Extraction → Text Cleaning → LLM Summarization → Display Results
```

**Symptom Checking:**
```
User Symptoms → Text Embedding → Vector Search (RAG) → Context Retrieval → 
LLM Analysis → Risk Assessment → Display Results with Citations
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Angular 17
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **UI Components**: Angular Material (optional)
- **HTTP Client**: Angular HttpClient
- **File Handling**: FileReader API

### Backend
- **Framework**: Flask 3.0
- **Language**: Python 3.9+
- **CORS**: Flask-CORS
- **OCR**: Tesseract OCR / EasyOCR
- **PDF Processing**: PyPDF2
- **LLM Integration**: LangChain
- **Vector Store**: ChromaDB / FAISS
- **Embeddings**: SentenceTransformers
- **LLM APIs**: Google Gemini / OpenAI GPT / Llama 3

### AI/ML Components
- **LLM**: Generative AI for summarization and analysis
- **RAG**: Retrieval Augmented Generation for grounded responses
- **OCR**: Optical Character Recognition for document digitization
- **Vector Database**: Semantic search over medical knowledge

---

## 📂 Project Structure

### Frontend Structure
```
frontend/
├── package.json
├── angular.json
├── tailwind.config.js
└── src/
    ├── app/
    │   ├── components/
    │   │   ├── navbar/
    │   │   │   ├── navbar.component.ts
    │   │   │   └── navbar.component.html
    │   │   ├── upload-report/
    │   │   │   ├── upload-report.component.ts
    │   │   │   └── upload-report.component.html
    │   │   ├── report-summary/
    │   │   │   ├── report-summary.component.ts
    │   │   │   └── report-summary.component.html
    │   │   ├── symptom-checker/
    │   │   │   ├── symptom-checker.component.ts
    │   │   │   └── symptom-checker.component.html
    │   │   ├── loader/
    │   │   ├── error-dialog/
    │   │   └── result-card/
    │   ├── services/
    │   │   ├── api.service.ts
    │   │   └── file-upload.service.ts
    │   ├── pages/
    │   │   ├── home/
    │   │   ├── report/
    │   │   ├── symptoms/
    │   │   └── dashboard/
    │   ├── app-routing.module.ts
    │   └── app.component.ts
    ├── assets/
    └── index.html
```

### Backend Structure
```
backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration settings
├── routes/
│   ├── __init__.py
│   ├── summarize.py           # Report summarization endpoints
│   ├── symptoms.py            # Symptom checker endpoints
│   └── ocr.py                 # OCR processing endpoints
├── services/
│   ├── __init__.py
│   ├── ocr_service.py         # OCR logic (Tesseract/EasyOCR)
│   ├── llm_service.py         # LLM interaction and prompts
│   ├── rag_service.py         # RAG pipeline and vector search
│   └── text_cleaner.py        # Text preprocessing utilities
├── database/
│   ├── embeddings/            # Generated vector embeddings
│   ├── vectorstore/           # ChromaDB/FAISS storage
│   └── dataset_loader.py      # Medical dataset initialization
├── uploads/                    # Temporary file storage
├── utils/
│   ├── pdf_reader.py          # PDF text extraction
│   └── formatters.py          # Response formatting
└── tests/                      # Unit and integration tests
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.9+
- **Tesseract OCR** installed on system
- **API Keys** for LLM service (Gemini/OpenAI)

### Installation

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/medisense-ai.git
cd medisense-ai
```

#### 2️⃣ Frontend Setup
```bash
cd frontend
npm install
```

**Configure Environment** (`src/environments/environment.ts`):
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000/api'
};
```

**Run Development Server**:
```bash
ng serve
```
Access at `http://localhost:4200`

#### 3️⃣ Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Install Tesseract OCR**:
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **MacOS**: `brew install tesseract`
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

**Configure Environment** (`config.py`):
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    CHROMA_DB_PATH = 'database/vectorstore'
```

**Initialize RAG Database**:
```bash
python database/dataset_loader.py
```

**Run Flask Server**:
```bash
python app.py
```
Access at `http://localhost:5000`

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. OCR Text Extraction
```http
POST /api/ocr
Content-Type: multipart/form-data

Parameters:
  - file: PDF or image file (required)

Response:
{
  "success": true,
  "extracted_text": "Patient Name: John Doe...",
  "confidence": 0.92
}
```

#### 2. Report Summarization
```http
POST /api/summarize
Content-Type: application/json

Body:
{
  "text": "Medical report text here..."
}

Response:
{
  "success": true,
  "patient_summary": "You were diagnosed with...",
  "doctor_summary": "Patient presents with...",
  "key_findings": [
    "Primary diagnosis: Type 2 Diabetes",
    "HbA1c: 7.8% (elevated)"
  ],
  "medications": ["Metformin 500mg", "Lisinopril 10mg"],
  "critical_warnings": ["Monitor blood glucose daily"],
  "follow_up": "Schedule appointment in 3 months"
}
```

#### 3. Symptom Analysis
```http
POST /api/symptom-check
Content-Type: application/json

Body:
{
  "symptoms": "fever, persistent cough, body aches for 3 days"
}

Response:
{
  "success": true,
  "possible_conditions": [
    {
      "name": "Influenza (Flu)",
      "probability": "high",
      "description": "Viral infection affecting respiratory system"
    },
    {
      "name": "COVID-19",
      "probability": "medium",
      "description": "Coronavirus infection with similar symptoms"
    }
  ],
  "urgency": "medium",
  "explanation": "Your symptoms suggest a viral respiratory infection...",
  "recommendations": [
    "Rest and hydration",
    "Monitor temperature",
    "Consider COVID-19 testing"
  ],
  "citations": [
    "WHO - Influenza (Seasonal)",
    "NIH MedlinePlus - Flu Symptoms"
  ],
  "seek_immediate_care_if": [
    "Difficulty breathing",
    "Persistent chest pain",
    "Confusion or severe dizziness"
  ]
}
```

---

## 🗄️ Dataset & RAG Pipeline

### Medical Knowledge Base

**Sources:**
- **WHO**: Disease descriptions and classifications
- **NIH MedlinePlus**: Patient-friendly medical information
- **Open Medical Datasets**: Symptom-disease mappings

**Structure:**
```json
{
  "disease": "Type 2 Diabetes",
  "symptoms": ["increased thirst", "frequent urination", "fatigue"],
  "causes": ["insulin resistance", "genetic factors"],
  "severity": "chronic",
  "source": "WHO"
}
```

### RAG Implementation

**Pipeline Steps:**

1. **Data Preparation**
   ```python
   # Load and chunk medical documents
   from langchain.text_splitter import RecursiveCharacterTextSplitter
   
   splitter = RecursiveCharacterTextSplitter(
       chunk_size=500,
       chunk_overlap=50
   )
   chunks = splitter.split_documents(medical_docs)
   ```

2. **Generate Embeddings**
   ```python
   from sentence_transformers import SentenceTransformer
   
   model = SentenceTransformer('all-MiniLM-L6-v2')
   embeddings = model.encode(chunks)
   ```

3. **Store in Vector Database**
   ```python
   import chromadb
   
   client = chromadb.PersistentClient(path="database/vectorstore")
   collection = client.create_collection("medical_knowledge")
   collection.add(embeddings=embeddings, documents=chunks)
   ```

4. **Retrieval & Generation**
   ```python
   # Query similar medical information
   results = collection.query(
       query_embeddings=query_embedding,
       n_results=5
   )
   
   # Pass to LLM with context
   context = "\n".join(results['documents'])
   prompt = f"Based on: {context}\nSymptoms: {user_symptoms}\nAnalyze:"
   ```

---

## 👥 Team

| Role | Responsibilities | Members |
|------|-----------------|---------|
| **Frontend Developers** | UI/UX, Angular components, API integration, responsive design | 2 members |
| **Backend Developers** | Flask APIs, OCR pipeline, database management, file handling | 2 members |
| **AI/ML Engineer** | LLM integration, prompt engineering, RAG pipeline, model optimization | 1 member |
| **QA/DevOps** | Testing, documentation, CI/CD, deployment, monitoring | 1 member |

---

## 🌐 Deployment (100% FREE for Hackathon)

### 🎯 Free Deployment Strategy

| Component | Platform | Free Tier | Perfect For |
|-----------|----------|-----------|-------------|
| Frontend | **Vercel** | Unlimited | Angular Apps |
| Backend | **Render** | 750 hrs/month | Flask APIs |
| Database | **Supabase** | 500MB | PostgreSQL |
| Vector DB | **Pinecone** | 1 index free | RAG embeddings |
| LLM API | **Google Gemini** | 60 req/min free | AI Processing |
| File Storage | **Cloudinary** | 25 GB free | Medical reports |

---

### 1️⃣ Frontend Deployment on Vercel (FREE)

**Step 1: Install Vercel CLI**
```bash
npm i -g vercel
```

**Step 2: Build and Deploy**
```bash
cd frontend
ng build --configuration production
cd dist/frontend
vercel --prod
```

**Or Use Vercel Dashboard:**
1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Configure build settings:
   - **Framework Preset**: Angular
   - **Build Command**: `ng build --configuration production`
   - **Output Directory**: `dist/frontend`
4. Click "Deploy"

**Environment Variables in Vercel:**
```
API_URL=https://your-backend.onrender.com/api
```

**vercel.json** (in frontend root):
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

### 2️⃣ Backend Deployment on Render (FREE)

**Step 1: Create render.yaml**
```yaml
services:
  - type: web
    name: medisense-backend
    env: python
    buildCommand: "pip install -r requirements.txt && apt-get update && apt-get install -y tesseract-ocr"
    startCommand: "gunicorn app:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: GEMINI_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

**Step 2: Deploy to Render**
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Select "Web Service"
4. Choose backend folder
5. Use these settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Add environment variables
7. Click "Create Web Service"

**requirements.txt** (add gunicorn):
```txt
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
pytesseract==0.3.10
pillow==10.1.0
PyPDF2==3.0.1
langchain==0.1.0
chromadb==0.4.18
sentence-transformers==2.2.2
google-generativeai==0.3.1
python-dotenv==1.0.0
```

---

### 3️⃣ Alternative: PythonAnywhere (100% FREE)

**Perfect for hackathons - No credit card required!**

**Step 1: Create Account**
- Visit [pythonanywhere.com](https://www.pythonanywhere.com)
- Sign up for free account (Beginner tier)

**Step 2: Upload Code**
```bash
# Via Git
git clone https://github.com/yourusername/medisense-ai.git
```

**Step 3: Setup Virtual Environment**
```bash
mkvirtualenv medisense --python=/usr/bin/python3.9
pip install -r requirements.txt
```

**Step 4: Configure Web App**
1. Go to "Web" tab
2. Add a new web app
3. Select "Manual Configuration" → Python 3.9
4. Set source code directory: `/home/yourusername/medisense-ai/backend`
5. Edit WSGI file:
```python
import sys
path = '/home/yourusername/medisense-ai/backend'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

**Step 5: Set Environment Variables**
- Go to "Files" → Edit `.env` file
```
GEMINI_API_KEY=your_key_here
SECRET_KEY=your_secret_key
```

**Your backend URL**: `https://yourusername.pythonanywhere.com`

---

### 4️⃣ Vector Database Setup (FREE)

#### Option A: Pinecone (Recommended for Hackathons)

**Step 1: Get Free API Key**
1. Visit [pinecone.io](https://www.pinecone.io)
2. Sign up → Get API key (1 index free forever)

**Step 2: Update Backend Code**
```python
# services/rag_service.py
import pinecone

pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment='gcp-starter'  # Free tier
)

index = pinecone.Index('medisense-knowledge')
```

#### Option B: ChromaDB (Local/Cloud)

For hackathons, use in-memory mode:
```python
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))
```

---

### 5️⃣ LLM API Setup (FREE)

#### Option A: Google Gemini (Best Free Option)

**Free Tier**: 60 requests/minute

**Step 1: Get API Key**
1. Visit [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Create API key (instant, no credit card)

**Step 2: Use in Backend**
```python
# services/llm_service.py
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(prompt)
```

#### Option B: Groq (Super Fast & Free)

**Free Tier**: 14,400 requests/day

```python
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": prompt}]
)
```

---

### 6️⃣ File Storage (FREE)

#### Cloudinary (Recommended)

**Free Tier**: 25 GB storage, 25 GB bandwidth/month

**Step 1: Setup**
```bash
pip install cloudinary
```

**Step 2: Configure**
```python
# config.py
import cloudinary

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)
```

**Step 3: Upload Files**
```python
from cloudinary.uploader import upload

result = upload(file, folder="medical_reports")
```

---

### 🚀 Complete Deployment Checklist

- [ ] Get Google Gemini API key (free)
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Render/PythonAnywhere
- [ ] Setup Pinecone vector database
- [ ] Configure Cloudinary for file storage
- [ ] Update frontend API URL
- [ ] Test all endpoints
- [ ] Add CORS headers
- [ ] Test file upload flow
- [ ] Test OCR processing
- [ ] Test symptom checker
- [ ] Create demo video

---

### 🔧 Environment Variables Summary

**Frontend (.env in Vercel):**
```
API_URL=https://your-backend.onrender.com/api
```

**Backend (.env in Render/PythonAnywhere):**
```
GEMINI_API_KEY=your_gemini_key
SECRET_KEY=your_secret_key_here
PINECONE_API_KEY=your_pinecone_key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
```

---

### 📊 Free Tier Limits (More than enough for hackathon!)

| Service | Free Limit | Hackathon Usage |
|---------|-----------|-----------------|
| Vercel | Unlimited deploys | ✅ Perfect |
| Render | 750 hours/month | ✅ 31 days free |
| Gemini | 60 req/min | ✅ 86,400 daily |
| Pinecone | 1 index, 100K vectors | ✅ Sufficient |
| Cloudinary | 25 GB storage | ✅ 1000s of files |
| PythonAnywhere | Always-on web app | ✅ 24/7 uptime |

---

### 🎥 Quick Deploy Commands

**Complete deployment in 5 minutes:**

```bash
# 1. Deploy Frontend
cd frontend
vercel --prod

# 2. Deploy Backend
cd ../backend
git push render main  # If using Render with Git

# 3. Initialize Vector DB
python database/dataset_loader.py

# Done! 🎉
```

---

## 🎬 Demo

### Sample Medical Report
Upload a blood test report or prescription, and receive:
- **Patient Summary**: "Your blood sugar levels are slightly elevated at 126 mg/dL, indicating prediabetes..."
- **Key Findings**: HbA1c 6.2%, Cholesterol 210 mg/dL
- **Recommendations**: Dietary modifications, exercise, follow-up in 6 months

### Sample Symptom Query
**Input**: "severe headache, sensitivity to light, nausea"

**Output**:
- Possible Conditions: Migraine (high probability), Tension headache (medium)
- Urgency: Medium
- Recommendations: Rest in dark room, hydration, OTC pain relief
- Red Flags: Seek immediate care if accompanied by fever, stiff neck, or vision changes

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python
- Use Angular style guide for TypeScript
- Write unit tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**MediSense AI is an educational/hackathon project and should NOT be used as a substitute for professional medical advice, diagnosis, or treatment.** Always consult qualified healthcare providers for medical concerns.

---
