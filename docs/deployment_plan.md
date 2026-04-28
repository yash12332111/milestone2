# FundFacts AI - Deployment Plan

## Architecture Overview
This application follows a modern decoupled architecture spanning 3 separate cloud platforms:
1. **Scheduler (Ingestion Pipeline)**: GitHub Actions
2. **Backend (FastAPI)**: Render
3. **Frontend (Next.js)**: Vercel

---

## 1. Vector Database (ChromaDB Cloud)
Before deploying the services, ensure the persistent cloud database is set up.
* **Platform**: [trychroma.com](https://www.trychroma.com/)
* **Steps**:
  1. Login to ChromaDB Cloud and create a new project/tenant.
  2. Create a new Database (`default_database`).
  3. Generate a Cloud API Key.
  4. Save the API Key, Endpoint, and Tenant Name. These will be required as environment variables for both the Backend and the Scheduler.

---

## 2. Scheduler & Data Ingestion (GitHub Actions)
The Knowledge Base Factory automatically scrapes and updates the vector database every day.

* **Platform**: GitHub Actions
* **Process**:
  1. Push the local code to a remote GitHub repository.
  2. Navigate to **Settings > Secrets and variables > Actions**.
  3. Add the following **Repository Secrets**:
     * `GROQ_API_KEY` (for LLM orchestration/embedding if needed)
     * `CHROMA_CLOUD_API_KEY`
  4. Add the following **Repository Variables**:
     * `CHROMA_TENANT`
     * `CHROMA_DATABASE`
  5. The workflow is already configured in `.github/workflows/daily_ingest.yml`.
  6. **Verification**: Go to the "Actions" tab in GitHub and click "Run workflow" manually to verify scraping, chunking, embedding, and ChromaDB upsert succeeds.

---

## 3. Backend Deployment (Render)
The FastAPI RAG server requires a Python web service environment.

* **Platform**: Render.com
* **Steps**:
  1. Create a Render account and click **New > Web Service**.
  2. Connect your GitHub repository.
  3. **Build Settings**:
     * **Environment**: `Python 3`
     * **Root Directory**: `.` (or leave blank if repository root)
     * **Build Command**: `pip install -r requirements.txt`
     * **Start Command**: `uvicorn phase3_api_server.main:app --host 0.0.0.0 --port $PORT`
  4. **Environment Variables**:
     * `GROQ_API_KEY`
     * `CHROMA_CLOUD_ENDPOINT`
     * `CHROMA_CLOUD_API_KEY`
     * `CHROMA_TENANT`
     * `CHROMA_DATABASE`
  5. **Free Tier Considerations**: Remember that Render's free tier spins down after 15 minutes of inactivity. Initial chat queries after a spin-down may take ~30-50 seconds.
  6. **CORS Configuration**: Once Vercel gives you a frontend URL, make sure to add it to the CORS `allow_origins` array in `phase3_api_server/main.py`.

---

## 4. Frontend Deployment (Vercel)
The Next.js Premium Editorial v2 application.

* **Platform**: Vercel.com
* **Steps**:
  1. Create a Vercel account and click **Add New > Project**.
  2. Import your GitHub repository.
  3. **Configuration**: 
     * **Framework Preset**: Next.js
     * **Root Directory**: `phase4_frontend`
     * **Build Command**: `npm run build`
     * **Install Command**: `npm install`
  4. **Environment Variables**:
     * `NEXT_PUBLIC_API_URL`: Set this to your live Render backend URL (e.g., `https://fundfacts-api.onrender.com`).
  5. Click **Deploy**.
  6. **Verification**: Visit the `.vercel.app` link. Check if the Premium UI loads correctly and that chat queries are communicating with the Render backend successfully.

---

## 5. Post-Deployment Checklist
- [ ] **Data Pipeline**: Run the GitHub Actions workflow manually. Did ChromaDB receive the 17 chunks?
- [ ] **Backend API**: Open the Render URL (e.g., `<URL>/health`). Does it return `{"status": "healthy"}`?
- [ ] **Frontend**: Go to the Vercel URL. Do the Hero fade-ups, Market Pulse widgets, and Chat interface load securely (HTTPS)?
- [ ] **End-to-End**: Type a query in the frontend chat (e.g., "What is the expense ratio?"). Did it hit the Render API securely, pull from ChromaDB Cloud, and return the answer?
