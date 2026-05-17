# Runnable Workshops

These are the hands-on exercises for the LSEG training day.

## Workshop 1: Compliance Document Agent

```bash
cd workshop1-compliance
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

Expected demo result: a compliance impact report with source references, action items, and a quality gate.

## Workshop 2: Multi-Agent Ticket Review

```bash
cd workshop2-ticket-review
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

Expected demo result: three sample tickets are reviewed by parser, quality, and knowledge agents, then routed by risk tier.

## Workshop 3: Copilot + SDD Meeting Agent

```bash
cd workshop3-copilot-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

Expected demo result: a structured meeting-minutes report plus a quality check generated from the same spec.

## API Keys

All workshops include a demo or mock path. Azure OpenAI keys are optional.

To enable model-backed execution:

```bash
cp .env.example .env
# edit .env with Azure OpenAI endpoint, deployment, and key
```

