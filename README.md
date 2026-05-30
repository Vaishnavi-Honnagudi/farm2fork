# 🌾 Farm-to-Fork Supply Chain Traceability System
### PS-A9 | FSSAI MRL Compliance · GenAI Narrative Reports · QR Certificates

---

## Project Overview

A GenAI-powered traceability system where farmers log crop inputs and the system automatically:
1. Checks FSSAI Maximum Residue Limits (MRL) for all pesticides used
2. Generates a professional DOCX traceability report with an AI-written narrative
3. Creates a QR code linking to the digital batch certificate

**Demo Produce:** Tomato · Leafy Greens · Rice

---

## Project Structure

```
farm2fork/
├── app.py               ← Streamlit web application (main UI)
├── demo_run.py          ← Standalone demo for all 3 crops (no UI)
├── fssai_mrl.py         ← FSSAI MRL database + compliance checker
├── report_generator.py  ← DOCX report builder (python-docx)
├── qr_generator.py      ← QR code generator (qrcode + Pillow)
├── llm_narrative.py     ← AI narrative via Anthropic API (Claude)
├── demo_data.py         ← Sample data: Tomato, Leafy Greens, Rice
├── requirements.txt     ← Python dependencies
├── reports/             ← Generated DOCX reports (auto-created)
└── qrcodes/             ← Generated QR PNG images (auto-created)
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key
```bash
# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

### 3a. Run the Streamlit web app
```bash
streamlit run app.py
```

### 3b. Run standalone demo (CLI)
```bash
python demo_run.py
```

---

## How It Works

### Module 1 — FSSAI MRL Compliance (`fssai_mrl.py`)
- Maintains a curated database of FSSAI Maximum Residue Limits for 12+ pesticides per crop
- `check_compliance(crop, pesticides)` returns PASS/FAIL/NOT_IN_DB for each pesticide
- Hazard levels: LOW / MEDIUM / HIGH based on pesticide class
- Reference: FSSAI Food Safety & Standards (Contaminants, Toxins and Residues) Regulations, 2011

### Module 2 — DOCX Report Generator (`report_generator.py`)
Generates a professional Word document with:
- Farm & batch information table
- Fertiliser and pesticide input log
- FSSAI compliance table (colour-coded: green=PASS, red=FAIL)
- AI narrative section
- Declarations and signature blocks

### Module 3 — QR Code Generator (`qr_generator.py`)
- Encodes batch metadata (ID, crop, farmer, location, harvest date) + verify URL
- Styled with rounded modules and FSSAI-green colour scheme
- Error correction level H (30% damage tolerance)

### Module 4 — AI Narrative (`llm_narrative.py`)
- Calls Claude (claude-opus-4-5) via Anthropic API
- Produces a formal 4-paragraph traceability narrative covering:
  - Origin and cultivation practices
  - Inputs and pest management
  - FSSAI compliance results
  - Consumer safety assurance

---

## Demo Results

| Crop | Batch ID | FSSAI Status | Risk | Key Finding |
|------|----------|-------------|------|-------------|
| 🍅 Tomato | TOM-KA-2024-001 | ✅ COMPLIANT | LOW | All 4 pesticides within MRL |
| 🥬 Leafy Greens | SPG-MH-2024-007 | ❌ NON-COMPLIANT | HIGH | Chlorpyrifos exceeds MRL (0.08 > 0.05 mg/kg) |
| 🌾 Rice | RIC-AP-2024-012 | ✅ COMPLIANT | MEDIUM | 2 high-hazard pesticides within limits |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend  | Streamlit |
| AI Narrative | Anthropic Claude API (claude-opus-4-5) |
| DOCX Generation | python-docx |
| QR Code | qrcode + Pillow (StyledPilImage) |
| Data Processing | pandas |
| MRL Database | FSSAI Regulations 2011 (embedded) |

---

## FSSAI MRL Reference

Data sourced from:
- FSSAI Food Safety & Standards (Contaminants, Toxins and Residues) Regulations, 2011
- FSSAI Compendium of MRLs: https://fssai.gov.in/upload/uploadfiles/files/Compendium_MRL.pdf
- FAO Codex Alimentarius pesticide residues database

---

## Extending the System

To add more crops: edit `FSSAI_MRL_DB` in `fssai_mrl.py`
To add more demo batches: edit `DEMO_PRODUCE` in `demo_data.py`
To customise the DOCX layout: edit `generate_report()` in `report_generator.py`
