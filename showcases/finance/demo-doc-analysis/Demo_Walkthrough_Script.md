# MAS Document Analysis Pipeline — Demo Walkthrough Script

> **Format:** Screen recording with narration (~5 minutes)
> **Language:** English
> **Deliverables:** This script + screen recording + slides/04_Sarah_Demo.pdf (background deck)

---

## [0:00–0:40] Opening — The Problem

Hi, this is a walkthrough of our MAS Regulatory Document Analysis Pipeline.

Here's the problem we're solving. Compliance analysts at MAS-regulated banks spend the majority of their time — up to 80% — on manual document processing. When MAS publishes a revised notice, someone has to read every page, compare it to the previous version, extract all the obligations, figure out which products are affected, and write an impact assessment. For a 47-page notice, that's 2 to 3 days of work. And if you miss even one clause — especially one buried in an annex — the consequences can be severe. DBS was fined 2.1 million dollars by MAS in 2023 for compliance failures.

Our AI Agent pipeline transforms this from a 3-day manual process into a 50-minute review workflow.

---

## [0:40–1:10] Meet Sarah Chen — The Persona

*[Show the app landing page — Sarah's challenge quote visible]*

Let me introduce our user. Sarah Chen is a compliance analyst at Horizon Bank Singapore, a mid-sized MAS-regulated bank. She has 6 years of experience. She's skilled and thorough.

It's Monday morning. MAS published a revised Notice FAA-N16 — "Recommendations on Investment Products" — over the weekend. 47 pages. Her manager wants an impact assessment by Wednesday.

Normally, Sarah would spend 16 to 23 hours across 5 manual steps: reading PDFs, doing side-by-side comparisons in Word, copying clauses into Excel, emailing department heads, and writing the report.

With our pipeline, she reviews AI-generated outputs instead. Same 5 steps — but the AI does the processing, and Sarah does the thinking.

*[Click "Start Pipeline Demo"]*

---

## [1:10–1:50] Step 1 — Download & Read (Document Ingestion Agent)

*[Step 1 results appear — metadata and parsed structure]*

**Step 1: the Document Ingestion Agent.**

The agent monitors the MAS website continuously. It detected this revised notice on Friday night at 10:15 PM, downloaded the PDF, and parsed the full document structure automatically.

What you see here is the output: 47 pages, 8 main sections plus 3 annexes, 52 clauses detected, over 18,000 words. The agent has parsed everything — sections, tables, figures — and preserved the document hierarchy.

Under the hood, this uses a web crawler for detection, a layout parser for document structure, OCR capability for scanned documents, and an LLM for structural parsing.

Sarah's time on this step: zero minutes. The document was ready when she logged in Monday morning.

*[Click "Mark as Reviewed → Proceed to Step 2"]*

---

## [1:50–2:40] Step 2 — Compare Versions (Version Comparison Agent)

*[Step 2 results appear — diff summary with added/modified/removed]*

**Step 2: the Version Comparison Agent.**

This is where the AI adds significant value. The agent retrieves the previous version of FAA-N16 from our knowledge base and performs a clause-level semantic comparison — not a simple text diff.

This matters because MAS often restructures sections between versions. A traditional diff tool would flag everything as changed. Our agent understands that a clause moved from Section 4 to Section 6 but is substantively the same, and it handles that correctly.

The results: 3 clauses added, 8 modified, 1 removed. You can see each change categorized by type and rated by significance.

Now here's the **explainability** feature — and this is critical for building trust in a compliance tool. If I click "Locate in Document" on any change, the right panel shows me the exact source text from both the old and new versions, with the relevant passage highlighted. Sarah can verify every AI finding against the original document. Nothing is a black box.

Sarah's time: 5 minutes to review the change summary.

*[Click "Mark as Reviewed → Proceed to Step 3"]*

---

## [2:40–3:30] Step 3 — Extract Obligations (Obligation Extraction Agent)

*[Step 3 results appear — obligation list with severity ratings]*

**Step 3: the Obligation Extraction Agent.**

The agent scans every clause for mandatory language — "shall," "must," "required" — and extracts all regulatory obligations. It found 26 obligations in this document, categorized by type and rated by severity: critical, high, or medium.

The technology here is a combination of domain-adapted Named Entity Recognition and LLM-based classification. This is not just keyword matching. The model understands context — "financial adviser shall ensure" is an obligation, but "the previous version shall be superseded" is not.

Again, the explainability layer: click "Locate in Document" on any obligation, and the right panel shows you the exact clause in the source document with the mandatory language highlighted. Every extraction is traceable to its source — this is essential for regulatory audit.

The model achieves 93%+ precision and 94%+ recall, benchmarked against legal expert annotations. This accuracy level is what separates a research-grade system from a vibe-coded demo.

Sarah's time: 10 minutes to review and validate.

*[Click "Mark as Reviewed → Proceed to Step 4"]*

---

## [3:30–4:15] Step 4 — Map to Products (Impact Mapping Agent)

*[Step 4 results appear — product impact cards]*

**Step 4: the Impact Mapping Agent.**

This step maps each obligation to the bank's actual product portfolio. You can see the bank has several products — structured deposits, investment funds, insurance products — and the agent has assessed the impact level for each.

The mapping uses a regulatory knowledge graph — built on Neo4j — that encodes the relationships between obligations, product types, departments, and compliance requirements. When the agent finds a new obligation about, say, enhanced CKA requirements for complex products, it automatically identifies which products in the bank's portfolio are classified as complex and flags them.

Click "View Regulatory Sources" on any product, and the right panel shows the full product profile — its classification, risk features, why it's affected — along with the specific regulatory source sections. This gives Sarah full transparency into the AI's reasoning. She can see exactly why a product was flagged as HIGH impact and verify it herself.

Previously, Sarah would email department heads and wait 2 days for replies. Now the draft mapping is instant, and Sarah applies her institutional knowledge to refine it.

Sarah's time: 15 minutes to review and adjust.

*[Click "Mark as Reviewed → Proceed to Step 5"]*

---

## [4:15–5:00] Step 5 — Generate Report (Impact Assessment Generator)

*[Step 5 results appear — executive summary, risk heat map, action items]*

**Step 5: the Impact Assessment Generator.**

The agent produces a full impact assessment report. You can see the executive summary, a compliance readiness score, a risk heat map broken down by product and risk category, and prioritized action items with owners, deadlines, and cost estimates.

Every statement in this report cites a specific clause from the MAS notice. This traceability is fundamental — when management asks "why do we need to update our CKA process?", the report points directly to Section 4.4, clause 4.4(a) of the revised notice. This provenance chain — from recommendation back to source clause — is what makes our tool trustworthy for compliance use.

Sarah can download the report, edit it, and submit to management. Her time: 20 minutes for editing.

*[Balloons animation — pipeline complete]*

---

## [5:00–5:30] Closing — The Result

Let me summarize. Same 5 steps Sarah always does — but instead of 2 to 3 days, it's 50 minutes. Instead of a 40% chance of missing clauses in annexes, we get over 93% recall.

The architecture: LangGraph for pipeline orchestration, Claude and GPT-4 for document understanding, fine-tuned NER for obligation extraction, Milvus vector database for semantic search, and Neo4j knowledge graph for product-regulation mapping.

But the key differentiator is not the pipeline itself — it's the explainability. Every AI output is traceable to its source, every finding is verifiable, and Sarah stays in the loop at every step. The AI does the processing. Sarah does the thinking. She submits Monday afternoon — not Wednesday.

Thank you.

---

## Accompanying Materials

- **Background slides:** [04_Sarah_Demo.pdf](../slides/04_Sarah_Demo.pdf) — 16 slides covering persona, problem statement, 5-step pipeline detail, technical architecture, and A*Star research roadmap
- **Demo app:** `cd demo-doc-analysis && streamlit run app.py`
