# MAS Document Analysis Pipeline — Demo

AI Agent demo for regulatory document analysis, focused on one user story:
**Sarah Chen**, a compliance analyst who needs to assess a revised MAS Notice.

## 5-Step Interactive Pipeline

1. **Download & Read** — Auto-ingest MAS Notice FAA-N16 (47 pages)
2. **Compare Versions** — Semantic clause-level diff (old vs new)
3. **Extract Obligations** — Find all shall/must/required clauses (26 obligations)
4. **Map to Products** — Map obligations to bank's product portfolio
5. **Generate Report** — Impact assessment with citations and action items

## Quick Start

```bash
pip install streamlit
streamlit run app.py
# Opens http://localhost:8501
```

## Key Features

- Step-by-step pipeline — user reviews each step before proceeding
- Realistic MAS FAA-N16 content (paraphrased from real regulation)
- Simulated AI outputs (no API keys required)
- Professional UI with progress tracking
- Downloadable impact assessment report

## Files

- `app.py` — Main Streamlit application
- `mas_documents.py` — MAS document content (old + new FAA-N16), Sarah's persona, bank products
- `pipeline_data.py` — Pre-computed AI outputs for all 5 pipeline steps
- `requirements.txt` — Dependencies (Streamlit only)

## Demo Context

This demo is designed for internal team presentation. Each step shows:
- What the AI agent does (automated processing)
- What Sarah sees (reviewable output)
- How much time Sarah saves vs manual process

**Manual: 16-23 hours (2-3 days) → AI Pipeline: 50 minutes (10x faster)**
