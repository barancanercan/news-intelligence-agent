
---

## 1. Scheduling Layer

**Responsibility:**
- Trigger news collection at fixed intervals.

**Characteristics:**
- Runs every 3 hours
- Stateless
- No decision-making logic

**Notes:**
- Scheduling does not depend on system load, news volume, or content.
- Failure to collect does not trigger retries with modified behavior.

---

## 2. Collection Layer

**Responsibility:**
- Gather political news content from across the web.

**Characteristics:**
- Passive ingestion
- No interpretation
- No filtering by credibility or ideology

**Collected Fields (conceptual):**
- URL
- Source domain
- Title
- Full text content
- Publication timestamp (if available)
- Collection timestamp

**Notes:**
- The collector treats the web as a noisy but valuable signal space.
- Coverage is prioritized over cleanliness.

---

## 3. Deduplication Layer

**Responsibility:**
- Prevent storing identical news items multiple times.

**Characteristics:**
- Deterministic
- Non-semantic
- Conservative (prefers false negatives over false positives)

**Signals Used:**
- URL hash
- Title hash + source
- Collection window checks

**Notes:**
- No embedding-based or semantic similarity is used.
- If duplication is uncertain, the item is preserved.

---

## 4. Storage Layer

**Responsibility:**
- Persist raw news data for downstream use.

**Characteristics:**
- Structured storage
- Raw text preservation
- Append-only behavior

**Design Principles:**
- No summarization at write time
- No semantic transformation
- No irreversible preprocessing

**Rationale:**
Raw storage maximizes compatibility with:
- LLM prompting
- Fine-tuning datasets
- RAG pipelines
- Future analytical layers

---

## 5. On-Demand Reporting Layer

**Responsibility:**
- Generate a unified intelligence report when explicitly requested.

**Trigger:**
- Manual human request only

**Process:**
1. Retrieve relevant news from storage (time-window based)
2. Rank items using quantitative importance signals
3. Condense content into a single report
4. Output neutral, broadcast-style text

**Importance Signals (non-exhaustive):**
- Frequency across sources
- Temporal concentration
- Source diversity
- Recency

**Notes:**
- The agent does not explain why items are important.
- Chronology is secondary to importance.

---

## Autonomy Boundaries

The system intentionally avoids:

- Autonomous decision-making
- Continuous analysis
- Alerting or push-based behavior
- Self-triggered summarization

Human input is required to move from **data collection** to **reasoning**.

---

## Downstream Integration

The architecture is designed to feed:

- Political intelligence systems
- Fine-tuning pipelines
- Dataset generation workflows
- Retrieval-Augmented Generation (RAG) systems

The agent itself remains upstream and neutral.

---

## Design Philosophy

- Separation of concerns over clever abstractions
- Determinism over adaptive behavior
- Passive collection before active reasoning
- Human-in-the-loop by default

