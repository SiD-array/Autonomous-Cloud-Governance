# Budget-Aware AI Squad 🤖💰

**Proactive Governance for the Agentic Cloud**

> Traditional FinOps is reactive—you find out about a $5,000 bill 48 hours too late. In the era of autonomous agents, costs can spiral in seconds.

Budget-Aware AI Squad is a decentralized framework that integrates **financial self-awareness** into AI agent meshes. It acts as a "Fiscal Guardrail," ensuring that autonomous systems stay within budget while maintaining high task performance.

---

## ✨ Key Capabilities

| Feature | Description |
|---------|-------------|
| 🛡️ **Agentic Circuit Breakers** | Automatically halts recursive agent "chatter" before budgets are exceeded |
| ⚖️ **Dynamic Model Routing** | Intelligently switches between local SLMs (via Ollama) and frontier LLMs based on task complexity and remaining funds |
| 📈 **Real-time Telemetry** | Dashboard for unit-cost-per-task tracking (UCST), shifting from infrastructure monitoring to agentic monitoring |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SUPERVISOR AGENT                         │
│               (Orchestrator & Handover Manager)              │
└──────────────────┬──────────────────────┬───────────────────┘
                   │                      │
                   ▼                      ▼
┌──────────────────────────┐    ┌──────────────────────────────┐
│    ACCOUNTANT AGENT      │◄───│       RESEARCHER AGENT       │
│   (Financial Gatekeeper) │    │    (Cloud Worker / Boto3)    │
│                          │    │                              │
│   • Circuit Breaker      │    │   • Interacts with LocalStack│
│   • Budget Validation    │    │   • BLOCKED until approved   │
│   • Spend Forecasting    │    │                              │
└──────────────────────────┘    └──────────────────────────────┘
                   │
                   ▼
          ┌───────────────┐
          │   LLM BRAIN   │ ◄─── brain.py
          │   (Ollama)    │
          └───────────────┘
```

### The Squad Members

- **Supervisor Agent**: Orchestrates the workflow and handles handovers between agents
- **Accountant Agent**: The "Financial Gatekeeper" — implements Agentic Circuit Breakers. No task can execute unless the Accountant validates the forecasted spend against remaining budget
- **Researcher Agent**: The "Cloud Worker" — uses Boto3 to interact with cloud infrastructure but must wait for Accountant approval

---

## 🛠️ Tech Stack

| Component | Technology | Endpoint |
|-----------|------------|----------|
| Local LLM | Ollama (Llama 3.1) | `http://localhost:11434` |
| Cloud Simulation | LocalStack | `http://localhost:4566` |
| Language | Python 3.14 | Windows/Linux/macOS |

---

## 📁 Project Structure

```
Autonomous-Cloud-Governance/
├── brain.py          # Central LLM interface ("Voice Box" for agents)
├── bridge.py         # Phase 1: Digital Office milestone
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

### Core Modules

#### `brain.py` - The Voice Box
Central LLM interface for all agents. Features:
- `LLMBrain` class for structured LLM interactions
- `ask_llama()` convenience function for quick queries
- **Cost simulation**: Tracks token usage at $0.015/1k tokens
- Fiscal ledger for budget-aware operations

#### `bridge.py` - Phase 1 Milestone
Demonstrates the foundational AI-to-cloud connection:
- Generates content via local LLM (Ollama)
- Stores artifacts in simulated S3 (LocalStack)
- **Zero cloud cost** proof of concept

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.14+** installed
2. **Ollama** installed and running
3. **LocalStack** installed and running

### Installation

```bash
# Clone the repository
git clone https://github.com/SiD-array/Autonomous-Cloud-Governance.git
cd Autonomous-Cloud-Governance

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Start Required Services

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Pull the model (first time only)
ollama pull llama3.1

# Terminal 3: Start LocalStack
localstack start
```

### Run Phase 1 Milestone

```bash
# Test the LLM Brain connection
python brain.py

# Run the Digital Office milestone
python bridge.py
```

---

## 📊 Cost Simulation

The system simulates costs to enable budget governance:

| Metric | Value |
|--------|-------|
| Token estimation | ~1 token per 4 characters |
| Cost rate | $0.015 per 1,000 tokens |
| Actual cloud cost | $0.00 (LocalStack simulation) |
| Actual LLM cost | $0.00 (Ollama local execution) |

---

## 🗺️ Roadmap

- [x] **Phase 1**: Digital Office — LLM + Cloud connection ($0.00)
- [ ] **Phase 2**: Accountant Agent — Budget circuit breakers
- [ ] **Phase 3**: Supervisor Agent — Multi-agent orchestration
- [ ] **Phase 4**: Real-time Telemetry Dashboard
- [ ] **Phase 5**: Production deployment with real AWS

---

## 📜 Architectural Principles

1. **Local First**: Always favor local execution (Ollama) to save costs
2. **Cost Awareness**: Log every token usage as simulated cost in the fiscal ledger
3. **Circuit Breakers**: No cloud action without Accountant approval
4. **Proactive Governance**: Forecast and approve costs BEFORE execution

---

## 🤝 Contributing

This is a course project for CSCI-750: Cloud Computing (Spring 2026).

---

## 📄 License

MIT License - See LICENSE file for details.

---

<p align="center">
  <i>Building fiscally responsible autonomous systems for the Agentic Era</i>
</p>
