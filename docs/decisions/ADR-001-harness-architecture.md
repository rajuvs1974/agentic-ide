# ADR-001: Harness Architecture

-   **Status:** Accepted
-   **Date:** 2026-09-03

## Context

The Agentic IDE needs to support autonomous software engineering tasks.

An agent should not directly control models, tools, workspace access, or
verification logic. Those capabilities need a controlled execution
environment that can enforce instructions, context, policies,
permissions, and verification.

## Decision

The project will implement a dedicated **Harness** as the control plane
surrounding agent execution.

The Harness is responsible for preparing, controlling, observing, and
verifying agent execution.

The Agent Runtime is responsible for executing an agent task using the
capabilities provided by the Harness.

## Responsibilities

### Harness

The Harness will eventually provide:

-   Instructions
-   Context
-   Tool registration and access
-   Execution state
-   Policies
-   Permissions
-   Verification
-   Evaluation
-   Execution metadata

### Agent Runtime

The Agent Runtime will:

-   Accept an agent task
-   Request execution context from the Harness
-   Execute the agent loop
-   Invoke permitted capabilities
-   Report execution state and results
-   Remain independent of FastAPI and model-provider implementations

### API Layer

FastAPI will provide the external interface between the IDE and backend
services.

The API layer should translate HTTP requests into domain objects and
should not contain agent execution logic.

## Initial Architecture

``` text
                    Code-OSS
                       |
                       v
                    FastAPI
                       |
                       v
                +--------------+
                | Agent Runtime|
                +------+-------+
                       |
                       v
                +--------------+
                |    Harness   |
                +------+-------+
                       |
          +------------+------------+
          v            v            v
       Context       Tools       Policies
          |            |            |
          +------------+------------+
                       |
                       v
                  Verification
```

## Initial Harness Components

The Harness will be developed incrementally:

1.  Execution Context
2.  Instructions
3.  Tool Registry
4.  Execution State
5.  Policy Engine
6.  Permission Manager
7.  Verification Engine
8.  Evaluation

## Design Principles

### Separation of concerns

The Agent Runtime must not become a monolithic component containing
tools, policies, permissions, model providers, and verification.

### Model independence

The Harness must not depend directly on a specific LLM provider.

### Tool control

Agents may only access tools explicitly made available by the Harness.

### Verification first

Agent-generated changes should be verified before being considered
successful.

### Observable execution

Agent execution should produce structured state and results so the IDE
can display progress and the evaluation system can measure outcomes.

### Incremental evolution

The Harness will start with a minimal deterministic implementation and
evolve toward autonomous execution without introducing unnecessary
complexity prematurely.

## Consequences

This architecture introduces additional abstractions, but provides a
foundation for:

-   Multiple model providers
-   Multiple agent types
-   Technology-specific skills
-   Tool permissions
-   Automated verification
-   Human approval
-   Agent evaluation
-   Multi-agent execution
-   Background agents
