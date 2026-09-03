# Agentic IDE

An open-source Agentic IDE foundation built around **Code-OSS**, **FastAPI**, **Agent Runtime**, and **Harness Engineering**.

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                       Agentic IDE                            │
│                                                             │
│  ┌──────────────────┐                                       │
│  │     Code-OSS     │  IDE / Editor Shell                   │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │     FastAPI      │  Backend API                          │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  Agent Runtime   │  Agent Execution                      │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │     Harness      │  Control Plane                        │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```text
agentic-ide/
├── code-oss/                  # Code-OSS editor foundation (separate git repo)
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── harness/
│   │       ├── context.py
│   │       ├── tool_registry.py
│   │       ├── tool_authorization.py
│   │       ├── instructions.py
│   │       ├── state.py
│   │       ├── policy.py
│   │       ├── policy_enforcement.py
│   │       ├── verification.py
│   │       ├── verification_engine.py
│   │       ├── evaluation.py
│   │       └── evaluation_engine.py
│   └── tests/
├── docs/
│   └── decisions/
│       └── ADR-001-harness-architecture.md
├── scripts/
│   └── verify.sh
└── README.md
```

## Current Capabilities

### FastAPI Backend

The backend currently provides:

- FastAPI application foundation
- Configuration management with Pydantic Settings
- Versioned Agent Task API
- Agent Runtime skeleton
- Typed domain models and API schemas
- Automated test, lint, and type-check verification

### Harness Engineering

The Agentic IDE uses a dedicated Harness layer to provide controlled, verifiable, and observable agent execution.

Current Harness components:

- **Harness Execution Context** — execution context and available capabilities
- **Tool Registry** — registration and discovery of tools
- **Tool Authorization** — explicit tool authorization
- **Harness Instructions** — model-independent execution instructions
- **Harness Execution State** — explicit execution lifecycle state
- **Harness Policy** — execution rules and constraints
- **Policy Enforcement** — enforcement of workspace and tool policies
- **Verification Results** — explicit PASS / FAIL verification results
- **Verification Engine** — aggregation of verification checks
- **Evaluation Results** — task evaluation results
- **Evaluation Engine** — deterministic evaluation score aggregation

The current Harness architecture is:

```text
                    HARNESS
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Context          Tools       Instructions
        │              │
        │       ┌──────┴──────┐
        │       ▼             ▼
        │    Registry    Authorization
        │                     │
        │                  Policy
        │                     │
        └──────────┬──────────┘
                   ▼
                State
                   │
                   ▼
             Verification
                   │
                   ▼
          Verification Engine
                   │
                   ▼
              Evaluation
                   │
                   ▼
           Evaluation Engine
```

### Verification-First Engineering

Agent completion is not treated as successful merely because the agent reports success.

The Harness is designed around explicit verification and evaluation:

```text
Agent Task
    │
    ▼
Execute
    │
    ▼
Verify
    │
    ├── PASS ──► Evaluate
    │
    └── FAIL ──► Remediate / Retry
```

Planned verification capabilities include:

- pytest
- Ruff
- Mypy
- Build verification
- Repository checks
- Task-specific validation
- Agent evaluation and benchmarking

## Development Philosophy

The project follows these principles:

1. **Harness before autonomy** — establish control and verification before adding powerful autonomous behavior.
2. **Verification first** — agent claims are not treated as proof of completion.
3. **Least privilege** — tools must be explicitly registered and authorized.
4. **Separation of concerns** — API, runtime, harness, tools, models, and verification remain independently testable.
5. **Model independence** — the Harness should not depend on a specific LLM provider.
6. **Incremental evolution** — build small, testable components before composing them into autonomous workflows.
7. **Observable execution** — execution state, verification, and evaluation should be inspectable.

## Verification

Run the complete backend verification workflow:

```bash
./scripts/verify.sh
```

This runs:

```text
pytest
  ↓
Ruff
  ↓
Mypy
```

All changes should pass the verification gate before being committed.

## Backend Development

The backend uses:

- Python 3.12+
- FastAPI
- Pydantic / Pydantic Settings
- uv
- Ruff
- Mypy
- Pytest

Example:

```bash
cd backend

uv sync

uv run pytest
uv run ruff check .
uv run mypy .
```

## Current Development Status

### Completed

- Code-OSS foundation
- FastAPI backend foundation
- Backend configuration
- Agent Task API
- Agent Runtime skeleton
- Harness architecture decision
- Harness Execution Context
- Harness Tool Registry
- Harness Tool Authorization
- Harness Instructions
- Harness Execution State
- Harness Policy
- Harness Policy Enforcement
- Harness Verification Result
- Harness Verification Engine
- Harness Evaluation Result
- Harness Evaluation Engine

### Next

The next phase is **Harness Integration**:

```text
Task
 ↓
Harness Context
 ↓
Instructions
 ↓
Policy
 ↓
Tool Authorization
 ↓
Execution State
 ↓
Agent Execution
 ↓
Verification
 ↓
Evaluation
 ↓
Final Result
```

The next planned task is **T012.1 — Harness Orchestrator**, which will compose the Harness components into a coherent execution flow.

## Long-Term Vision

The project is intended to evolve toward a full Agentic Engineering environment with:

- AI coding assistant
- Repository-aware agents
- Code intelligence
- Technology-specific engineering skills
- Controlled filesystem and terminal tools
- Automated test/fix/retest loops
- Git-aware workflows
- Human approval gates
- Agent evaluation and benchmarks
- Multi-agent collaboration
- Browser agents
- Background/cloud agents
- Multiple model providers

The immediate goal is a reliable, verification-first vertical slice rather than attempting to reproduce every capability of mature commercial Agentic IDEs at once.
