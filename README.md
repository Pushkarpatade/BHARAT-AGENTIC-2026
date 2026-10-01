# 🌾 BharatAgentic MSME Navigator

![Hackathon](https://img.shields.io/badge/Hackathon-BharatAgentic_2026-orange?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Tech-Groq_|_Qdrant_|_Streamlit-blue?style=for-the-badge)

**An autonomous, action-oriented AI agent built to replace expensive CAs and help rural MSMEs navigate government compliance, subsidies, and loans.**

---

## 🚀 The Problem
Grassroots entrepreneurs and rural MSMEs face massive hurdles navigating fragmented government portals (Aadhaar, Udyam, GST) and complex bureaucratic jargon. This friction prevents financial inclusion and forces small business owners to hire expensive middlemen or Chartered Accountants just to figure out their eligibility and apply for simple subsidies.

## 💡 Our Agentic Solution
Unlike basic information-retrieval chatbots, the **MSME Compliance Navigator** is a true autonomous workflow agent. It takes unstructured data, autonomously structures it, runs a simulated multi-dimensional compliance audit across government portals, and takes physical action by auto-drafting bureaucratic forms.

### ✨ Key Features (The Agentic Workflow)
1. **Perception (PDF Extraction):** Ingests business profile PDFs and uses **Groq's** high-speed LLM inference to parse unstructured data into a strict JSON profile.
2. **Reasoning (Central Verification Engine):** Runs deterministic logic to simulate multi-dimensional API checks across Gov portals (checking Aadhaar linkages, GST turnover exemptions, and Udyam status).
3. **Retrieval (RAG):** Uses a **Qdrant** Vector Database to accurately match the verified profile against live government schemes (e.g., MUDRA vs PMEGP).
4. **Execution (Auto-Drafter):** Closes the loop by acting as an automated CA, dynamically drafting pre-filled, print-ready official application forms.

---

## 🛠️ Technology Stack
* **Groq:** High-speed LLM Inference for unstructured data extraction and intent matching.
* **Qdrant:** Vector Database for scalable, semantic scheme matching.
* **Streamlit:** Interactive frontend UI and central verification dashboard.
* **Python:** Core backend logic and deterministic verification scripting.

---

## 💻 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/bharatagentic-msme-navigator.git
cd bharatagentic-msme-navigator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_CLUSTER_ENDPOINT=your_qdrant_url_here
```

### 4. Run the Agent
```bash
python -m streamlit run app.py
```
*Access the dashboard at `http://localhost:8501`*

---

## 📁 Repository Structure
* `app.py`: Streamlit frontend and UI orchestration.
* `agent.py`: Core agent logic, LLM extraction, verification engine, and Qdrant integration.
* `generate_pdf.py`: Script to generate a realistic demo MSME profile for testing.
* `aikart.yaml` / `manifest.yaml`: Deployment configurations for the aiKart platform.
* `msme_demo_profile.pdf`: A sample file to test the agent's extraction and verification capabilities.

---
*Built with ❤️ for the BharatAgentic 2026 Hackathon.*
