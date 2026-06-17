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

### Prerequisites
- **Docker** 24+ ([install](https://docs.docker.com/engine/install/))
- **Docker Compose** (included with Docker Desktop)
- 16 GB RAM minimum (32 GB recommended)

### Step 1 — Clone and Launch
```bash
git clone https://github.com/BaronTrump/manufacturing-agent-zero.git
cd manufacturing-agent-zero
docker compose -f docker/docker-compose.yml up -d
```

### Step 2 — Open the Web UI
Navigate to **http://localhost** in your browser.

### Step 3 — Configure an LLM
From the Web UI settings, choose one:

| Provider | Setup | Internet Required? |
|----------|-------|-------------------|
| **Ollama** (local) | `docker compose --profile local-llm up -d` then run `ollama pull llama3` inside the container | No (after initial pull) |
| **OpenAI / Anthropic** | Enter your API key in Settings | Yes |
| **Any OpenAI-compatible** | Point at your own server's `api_base` | Depends on your server |

### Step 4 — Select an Agent Profile
Click the agent selector in the top bar and choose from:
- Manufacturing Engineer, Quality Inspector, Production Planner, Maintenance Tech, or Purchasing Agent

### Step 5 — Start Working
Type your manufacturing question in the chat, for example:
> *"What is the PFMEA severity rating for a crack in a steering knuckle?"*
> *"Calculate OEE with 420 min planned time, 380 min run time, 45 sec cycle, 600 parts, 580 good parts"*
> *"Schedule preventive maintenance for CNC machine after 450 hours of operation"*

---

### Fully Air-Gapped / Offline Deployment
For a completely offline setup with no external API calls:

```bash
# Clone on a machine with internet, then transfer the directory
git clone https://github.com/BaronTrump/manufacturing-agent-zero.git

# Start both the agent and local LLM
docker compose --profile local-llm -f docker/docker-compose.yml up -d

# Pull a model (needs internet once)
docker compose exec ollama ollama pull llama3.1:8b

# Everything now runs locally — disconnect from the internet
# Configure Ollama as the LLM provider in the Web UI settings
```

### Windows Deployment
```powershell
git clone https://github.com/BaronTrump/manufacturing-agent-zero.git
cd manufacturing-agent-zero
docker compose -f docker/docker-compose.yml up -d
```
Then open **http://localhost** in your browser. For WSL2-backed Docker, ensure WSL2 integration is enabled in Docker Desktop settings.

### Production Deployment
For plant-floor deployment on a dedicated server or VM:

```bash
# Pull the latest
git pull && docker compose -f docker/docker-compose.yml build

# Run as a systemd service (Linux)
sudo tee /etc/systemd/system/manufacturing-agent.service <<'EOF'
[Unit]
Description=Manufacturing Agent Zero
After=docker.service

[Service]
WorkingDirectory=/opt/manufacturing-agent-zero
ExecStart=/usr/bin/docker compose -f docker/docker-compose.yml up
ExecStop=/usr/bin/docker compose -f docker/docker-compose.yml down
Restart=always
User=manufacturing

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now manufacturing-agent.service
```

### Updating
```bash
cd manufacturing-agent-zero
git pull
docker compose -f docker/docker-compose.yml build
docker compose -f docker/docker-compose.yml up -d
```

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
