# Technology Stack

This document describes the finalized technology stack for `news-intelligence-agent`.

All choices prioritize:
- Open-source software
- Zero vendor lock-in
- Deterministic behavior
- Long-term maintainability
- Compatibility with local LLM workflows (2026-ready)

This stack is considered **locked** unless a clear, system-level constraint emerges.

---

## Core Language

### Python 3.12

**Rationale:**
- Best ecosystem for web collection, text processing, and LLM integration
- Native compatibility with PyTorch and Hugging Face tooling
- Rapid iteration and “vibe coding” friendly
- Strong long-term OSS support

Python is used for:
- Crawling
- Deduplication
- Storage orchestration
- On-demand reporting

---

## Scheduling & Execution

### cron / systemd timers

**Rationale:**
- OS-native
- No external dependencies
- Predictable behavior
- Easy inspection and debugging

The agent:
- Collects data every 3 hours
- Does not self-trigger or adapt scheduling behavior

No task queues or workflow engines are used by design.

---

## Web Collection

### HTTP & Parsing
- `httpx`
- `beautifulsoup4`
- `readability-lxml`

**Rationale:**
- Fast, lightweight, and stable
- Suitable for text-heavy news content
- Avoids browser-based scraping complexity

### Discovery
- RSS feeds (when available)
- HTML search result parsing
- Keyword-based discovery

JavaScript rendering is intentionally avoided unless strictly necessary.

---

## Deduplication

### Deterministic Hashing
- Python `hashlib` (SHA-256)

**Signals used:**
- URL hash
- Title hash + source

**Rationale:**
- Deterministic
- Transparent
- Debuggable
- Avoids semantic ambiguity

Semantic or embedding-based deduplication is explicitly out of scope.

---

## Storage

### PostgreSQL 16

**Usage:**
- `TEXT` fields for raw content
- `TIMESTAMP` for temporal signals
- Optional `JSONB` for metadata

**Rationale:**
- Fully open source
- Battle-tested and production-grade
- Excellent support for large text fields
- Easy integration with future analytical layers

The database follows an **append-only philosophy**.

---

## Database Access Layer

### SQLAlchemy 2.x + psycopg3

**Rationale:**
- Explicit schema definition
- Clear separation between models and logic
- Migration support via Alembic (post Milestone-1)

Async behavior is not required at the current scale.

---

## Reporting & LLM Integration

### Local LLM Inference
- `llama.cpp` / `Ollama`
- Llama 3.x or Mistral-family models

**Rationale:**
- Fully local execution
- No API cost
- No data leakage
- Suitable for on-demand summarization

### Orchestration
- Plain Python prompts
- No agent frameworks

Frameworks intentionally avoided:
- LangChain
- CrewAI
- AutoGen

The system architecture already defines agent behavior explicitly.

---

## Configuration Management

### pydantic-settings + `.env`

**Rationale:**
- Explicit configuration
- Environment-safe
- Minimal cognitive overhead

---

## Logging & Inspection

### structlog

**Rationale:**
- Structured logs
- Human-readable output
- Suitable for both development and light production use

Advanced observability stacks are intentionally excluded.

---

## Explicit Non-Choices

The following technologies are intentionally NOT used:

- Cloud-managed services
- Vector databases (initially)
- Semantic search or embeddings
- Autonomous agent frameworks
- Browser automation (Playwright / Selenium)
- Task queues (Celery, Kafka, etc.)

These may be evaluated only after real-world usage justifies them.

---

## Summary

This stack favors:
- Simplicity over abstraction
- Determinism over autonomy
- Execution over speculation

It is designed to support a long-lived, inspectable, and extensible intelligence ingestion system.

