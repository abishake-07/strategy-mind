# StrategyMind

GenAI-powered strategy intelligence assistant for consulting use-cases.

Quick start

1. Copy `.env.example` to `.env` and fill secrets (Neo4j, Hugging Face keys).

2. Install dependencies (prefer a venv):

```bash
pip install -r requirements.txt
```

3. Seed Neo4j (if running locally):

```bash
python scripts/seed_neo4j.py
```

4. Add your PDFs to `data/pdfs/` and build the Chroma index:

```bash
python scripts/build_chroma.py --pdf-dir data/pdfs
```

5. Run the API server:

```bash
uvicorn api.main:app --reload --port 8000
```

6. Query the API:

```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query":"What AI strategies are automotive OEMs pursuing?"}'
```

Notes
- By default the system uses local `sentence-transformers` for embeddings and the Hugging Face Inference API for generation. Change behavior via `.env`.
