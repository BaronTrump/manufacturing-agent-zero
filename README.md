# Manufacturing Agent Zero

A localized, multilingual AI agent for industrial auto part manufacturers, built on [Agent Zero](https://github.com/agent0ai/agent-zero).

## Features

- **🎯 Manufacturing-Specific** — Pre-configured agent profiles for manufacturing engineer, quality inspector, production planner, maintenance technician, and purchasing agent
- **🌍 Multilingual** — Full support for English, Spanish, and Korean (ISO 639-1: en, es, ko)
- **🧠 Company Data Training** — On-premises RAG with FAISS vector database; train on your own manuals, specs, and quality records
- **🔧 Custom Manufacturing Tools** — OEE calculator, PLC interface, quality defect tracker, maintenance scheduler, supplier evaluation
- **🏭 Domain Knowledge** — Built-in knowledge base covering ISO/TS 16949, IATF 16949, APQP, PFMEA, SPC, MSA, PPAP, lean manufacturing, and more
- **🚀 Fully On-Premises** — Docker-based, all processing local, no cloud dependency
- **🔌 Extensible** — Plugin hub, MCP support, custom skills, and A2A connectors

## Quick Start

```bash
# macOS / Linux
curl -fsSL https://bash.manufacturing-agent.ai | bash

# Windows PowerShell
irm https://ps.manufacturing-agent.ai | iex

# Or with Docker directly:
docker run -p 80:80 \
  -v manufacturing_data:/a0/usr \
  -v company_kb:/a0/knowledge/company \
  barontrump/manufacturing-agent
```

Open the Web UI, select your agent profile, and start working.

## Architecture

```
manufacturing-agent/
├── agents/              # Agent profiles (manufacturing-specific)
│   ├── manufacturing-engineer/
│   ├── quality-inspector/
│   ├── production-planner/
│   ├── maintenance-tech/
│   └── purchasing-agent/
├── knowledge/           # Domain knowledge (RAG-ready)
│   ├── main/           # Core knowledge areas
│   │   ├── quality/    # ISO/TS 16949, SPC, MSA, PPAP
│   │   ├── processes/  # Casting, forging, machining, assembly
│   │   ├── safety/     # OSHA, machine guarding, LOTO
│   │   ├── standards/  # DIN, ASTM, SAE, JIS
│   │   ├── maintenance/# TPM, predictive, preventive
│   │   └── production/ # OEE, lean, JIT, kanban
│   └── solutions/      # Known solutions & troubleshooting
│       ├── defects/    # Porosity, cracks, dimensional issues
│       ├── optimization/# Cycle time, yield, throughput
│       └── troubleshooting/
├── tools/              # Custom manufacturing tools
├── prompts/            # System prompts (en, es, ko)
├── skills/             # Manufacturing-specific skills
├── plugins/            # Plugin configurations
├── docs/               # Documentation by language
│   ├── en/
│   ├── es/
│   └── ko/
└── data/               # On-premises data persistence
    ├── vector-store/   # FAISS index
    ├── company-kb/     # Company-specific documents
    └── config/         # Per-project configuration
```

## Agent Profiles

| Profile | Purpose | Key Tools |
|---------|---------|-----------|
| Manufacturing Engineer | Process design, fixture design, root cause analysis | CAD viewer, PFMEA, capability studies |
| Quality Inspector | Defect detection, SPC, PPAP, audit prep | Gauge R&R, control charts, CMM inspection |
| Production Planner | Scheduling, capacity planning, material flow | OEE, kanban, MRP interface |
| Maintenance Tech | Predictive/preventive maintenance, TPM | Vibration analysis, thermography, oil analysis |
| Purchasing Agent | Supplier evaluation, RFQ, contract review | Supplier scorecard, PPAP tracker, cost analysis |

## Multilingual Support

The agent interface is available in three languages:

- **English** (default) — ISO 639-1: `en`
- **Spanish** — ISO 639-1: `es`  
- **Korean** — ISO 639-1: `ko`

Switch languages from the Web UI settings dropdown. System prompts, tool descriptions, and domain knowledge are translated. Company-trained data is language-agnostic (vector embeddings).

## Training with Company Data

### Method 1: Upload via Web UI
1. Navigate to **Knowledge → Upload**
2. Drag and drop PDFs, DXF/STEP files, CSV quality logs, or SOP documents
3. The system automatically chunks, embeds, and indexes into FAISS

### Method 2: File System Drop
```bash
# Mount your company data directory
docker run -p 80:80 \
  -v /path/to/your/manuals:/a0/knowledge/company \
  -v manufacturing_data:/a0/usr \
  barontrump/manufacturing-agent
```

### Method 3: CLI Training Tool
```bash
docker exec -it manufacturing-agent python scripts/train.py \
  --source /data/company-kb \
  --language en \
  --chunk-size 512
```

## API

The agent exposes a REST API for integration with existing MES/ERP systems:

```bash
# Chat completion
POST /api/chat
{"message": "What is the OEE of line 3?", "language": "en"}

# Knowledge search
POST /api/knowledge/search
{"query": "porosity correction in aluminum casting", "top_k": 5}

# Company data training
POST /api/knowledge/ingest
{"source": "path/to/document.pdf", "metadata": {"area": "quality"}}
```

## Configuration

See `conf/` for:
- `model_providers.yaml` — LLM provider setup (Ollama, OpenAI-compatible, etc.)
- Per-agent configuration via `agents/<profile>/agent.yaml`

## On-Premises Requirements

- Docker (24+)
- 16 GB RAM minimum (32 GB recommended)
- GPU optional (NVIDIA CUDA for local LLMs)
- Disk: 50 GB for vector store + company data

## License

MIT — built on [Agent Zero](https://github.com/agent0ai/agent-zero) (MIT)
