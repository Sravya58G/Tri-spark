# StudyMate — PDF-Based AI Q&A (Hackathon Starter)

StudyMate is an AI-powered PDF Q&A assistant built for students. This repository is a complete hackathon-ready starter that implements the full pipeline described in the project brief: PDF ingestion, chunking, embedding + FAISS retrieval, prompt construction, Watsonx (Mixtral) integration placeholder, and a polished Streamlit UI with session history and transcript download.

> **Note:** This starter includes clear placeholders for IBM Watsonx API integration (`llm_client.py`). The app provides safe local fallbacks so you can test UI and retrieval without keys. To use Watsonx, add credentials to `.env` and follow the instructions below.

---

## What's included
- `streamlit_app.py` — Streamlit frontend with multi-PDF upload, question input, answer display, referenced paragraphs, session history, and transcript download.
- `studymate/` — Python package with modular code:
  - `pdf_parser.py` — PDF text extraction using PyMuPDF (fitz) and normalization.
  - `chunker.py` — Sliding-window chunk segmentation (500 words, 100 overlap configurable).
  - `embeddings_index.py` — Embedding creation (SentenceTransformers) and FAISS index handling (placeholders & safe behavior when models not available).
  - `retriever.py` — Query embedding + FAISS search logic.
  - `llm_client.py` — Watsonx API wrapper (placeholder) and a local safe generator fallback.
  - `session_store.py` — In-memory session logging and export utilities.
  - `utils.py` — helper utilities.
- `prompt_templates.md` — Prompt engineering templates (system + context + question) from the project spec.
- `.env.example` — Environment variables example for IBM keys.
- `requirements.txt` — All necessary Python packages.
- `LICENSE` — MIT
- `assets/` — small CSS and background used by Streamlit (inline use).

---

## Quick start (local)
1. Create Python 3.10+ venv and activate it.
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. (Optional) Add Watsonx credentials:
   - Copy `.env.example` -> `.env` and fill `IBM_API_KEY`, `IBM_URL`, `IBM_PROJECT_ID`
3. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```
4. Open the URL printed by Streamlit (usually http://localhost:8501)

---

## Implementation notes & hackathon tips
- Chunk size and overlap are configurable in `studymate/chunker.py`.
- FAISS index is stored in memory; you can extend to disk persistence (index.save/load).
- To get best results on Watsonx, keep prompt concise and include only top-k chunks (default k=3).
- Session transcript export is available via "Download Q&A History".
- For demo/demoing without IBM API, the app uses a safe local generator that synthesizes answers from retrieved text.

---

If you want, I can now:
- Wire the Watsonx API (if you paste credentials here, or allow me to add code using public API docs)
- Add a demo dataset of sample PDFs and prebuilt index (large models may be required to reproduce full behaviour)
- Deploy the app to Streamlit Cloud / Hugging Face Spaces (requires credentials)

Enjoy — good luck at your hackathon!

Generated on: 2025-09-12T19:11:24.237644 UTC
