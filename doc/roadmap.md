# Roadmap

This roadmap defines the incremental development plan for `news-intelligence-agent`.

The goal is not feature completeness, but **a working, inspectable, and extensible system** that can be evolved through real usage.

Each milestone must produce something that:
- runs
- can be inspected
- reduces ambiguity

---

## Milestone 0 — System Skeleton (Current)

**Status:** Completed

**Goal:**
Establish a clear mental and architectural model before writing production code.

**Outputs:**
- README.md
- agent_rules.md
- architecture.md
- data_model.md
- roadmap.md

**Definition of Done:**
- The agent’s role is unambiguous
- Scope boundaries are explicit
- No implementation decisions are locked prematurely

---

## Milestone 1 — Continuous News Collection

**Goal:**
Verify that the system can continuously collect and store news data without duplication.

**Key Capabilities:**
- Scheduled execution every 3 hours
- Web-wide news collection
- Deterministic deduplication
- Raw data persistence

**Deliverables:**
- Working collector module
- Deduplication logic
- Database schema initialization
- Ability to inspect collected raw news

**Success Criteria:**
- The system runs unattended
- Duplicate news items are not stored
- Raw text content is preserved intact

---

## Milestone 2 — On-Demand Unified Report

**Goal:**
Enable the agent to generate a single intelligence report when explicitly requested.

**Key Capabilities:**
- Manual trigger for report generation
- Retrieval of recent news from storage
- Importance-first ranking
- Neutral, broadcast-style reporting

**Deliverables:**
- Report generation pipeline
- Importance scoring logic (heuristic-based)
- Single unified text output

**Success Criteria:**
- No reports are generated autonomously
- Output is deterministic given the same data
- Report tone matches agent rules

---

## Milestone 3 — Stabilization & Inspection

**Goal:**
Make the system understandable, inspectable, and safe to extend.

**Key Capabilities:**
- Basic logging
- Simple configuration management
- Clear entry points for collection vs reporting

**Deliverables:**
- Configuration file(s)
- Minimal operational documentation
- Clear separation between ingestion and reasoning code paths

**Success Criteria:**
- A new contributor can understand the flow in under 30 minutes
- System behavior matches architectural documents

---

## Explicitly Out of Scope (For Now)

The following are intentionally postponed:

- Semantic deduplication
- Embeddings and vector databases
- Fact-checking or credibility scoring
- Autonomous alerts or triggers
- Fine-tuning or model training

These may be revisited only after real-world usage justifies them.

---

## Guiding Principle

> Build only what is necessary to move from **idea → running system → observed behavior**.

Learning, optimization, and abstraction must follow execution, not precede it.
