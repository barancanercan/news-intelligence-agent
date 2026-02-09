# Data Model

This document defines the conceptual data model for `news-intelligence-agent`.

The data model is designed to:
- Preserve raw information
- Support deterministic deduplication
- Maximize downstream LLM compatibility
- Avoid premature optimization or semantic coupling

---

## Design Principles

- Raw text preservation over preprocessing
- Append-only data philosophy
- Deterministic identifiers
- Schema clarity over flexibility
- Read-optimized for LLM consumption

---

## Core Entity: NewsItem

Each collected news article is stored as a single immutable record.

### Conceptual Fields

| Field | Type | Description |
|-----|-----|-------------|
| id | UUID | Unique internal identifier |
| collected_at | TIMESTAMP | When the agent collected the item |
| published_at | TIMESTAMP (nullable) | Original publication time, if available |
| source | TEXT | Source domain or publisher name |
| url | TEXT | Canonical URL of the news item |
| title | TEXT | Original headline |
| content | TEXT | Full raw text content |
| category | TEXT (nullable) | Optional coarse category (e.g. news, column) |
| url_hash | TEXT | Deterministic hash of the URL |
| title_hash | TEXT | Deterministic hash of the title |

---

## Deduplication Support Fields

Deduplication relies on **deterministic, non-semantic signals**.

### Primary Signals

- `url_hash`
- `title_hash + source`

### Design Rationale

- Hashes allow fast equality checks
- No semantic similarity is assumed
- False negatives are preferred over false positives
- Duplicate uncertainty results in preservation

---

## Temporal Fields

Two timestamps are intentionally separated:

- `published_at` → external signal
- `collected_at` → system truth

This allows:
- Recency-based ranking
- Backfill handling
- Re-collection analysis

---

## Importance Scoring (Derived, Not Stored)

Importance scores are **computed at read time**, not persisted.

Reasons:
- Scoring logic may evolve
- Raw data remains canonical
- Avoids retroactive data mutation

Signals used for scoring may include:
- Frequency across sources
- Temporal clustering
- Source diversity
- Recency

---

## Storage Characteristics

- Append-only writes
- No in-place updates of content
- No summarization or labeling at write time
- No embedding storage in the initial phase

---

## Explicit Non-Goals

The data model does NOT support:

- Fact verification metadata
- Credibility scoring
- Political labeling
- Sentiment analysis
- Opinion tagging

These concerns belong to downstream systems.

---

## Future Extensions (Out of Scope)

The following may be added later but are intentionally excluded now:

- Embedding tables
- Semantic similarity indexes
- Cross-document linkage
- Annotation layers

---

## Summary

This data model treats news as **raw intelligence signals**, not curated knowledge.

Interpretation, analysis, and judgment are deferred by design.

