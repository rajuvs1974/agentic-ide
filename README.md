# Agentic IDE

An experimental Agentic IDE built around **Code-OSS + FastAPI + Agent Runtime + Harness Engineering**.

The goal is to explore how modern AI coding environments can evolve from simple code assistants into autonomous software engineering systems.

## Architecture

```text
┌─────────────────────────────┐
│          Code-OSS            │
│        IDE / Editor          │
└──────────────┬──────────────┘
               │
               │ API
               ▼
┌─────────────────────────────┐
│           FastAPI            │
│          API Layer           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Agent Runtime          │
│                             │
│  Task → Execution → Result  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│           Harness            │
│                             │
│ Context • Tools • State     │
│ Policies • Verification     │
│ Permissions • Evaluation    │
└─────────────────────────────┘
