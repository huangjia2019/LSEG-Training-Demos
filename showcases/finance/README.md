# Finance Showcase Demos

These demos are better for instructor walkthroughs, screenshots, and general-audience sessions.

## MAS Document Analysis Pipeline

Folder: `demo-doc-analysis`

This is the newer and stronger showcase. It follows Sarah Chen, a compliance analyst, through a five-step regulatory document workflow:

1. Download and read the MAS notice.
2. Compare old and new versions.
3. Extract obligations.
4. Map obligations to products.
5. Generate an impact report.

Run:

```bash
cd demo-doc-analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## MAS Compliance Analyst Agent

Folder: `demo-MAS-analyst`

This is a broader V1-style gallery for compliance-manager tasks:

- Product compliance analysis.
- Interactive customer/product compliance check.
- Analyst task automation map.
- MAS regulation knowledge base.

Run:

```bash
cd demo-MAS-analyst
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## How To Use In Training

Use `demo-doc-analysis` in the first hour to give everyone a concrete picture of what a financial agent workflow looks like.

Use the CLI workshops later when the room shifts from "what can this do?" to "how should we design it safely?"

