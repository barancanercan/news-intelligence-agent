# news-intelligence-agent

A continuous political news ingestion agent that collects data from across the web at regular intervals, stores it without duplication, and generates a single, neutral intelligence report on demand.

## Overview

`news-intelligence-agent` is designed as a **background ingestion system**, not a chatbot or real-time analyst.  
It continuously gathers political news every 3 hours, preserves raw textual content, and produces structured summaries **only when explicitly requested by a human**.

The system prioritizes coverage and signal collection over interpretation, verification, or opinion.

## Core Principles

- Continuous collection, on-demand reasoning
- Neutral, broadcast-style reporting
- Importance-first, frequency-aware prioritization
- No interpretation, no opinion, no conclusions
- Raw data preservation for downstream systems

## What This Agent Does

- Collects political news from across the web every 3 hours
- Prevents duplicate data ingestion
- Stores raw news content in a structured database
- Generates a **single unified intelligence report** when requested
- Ranks news by quantitative importance signals (frequency, spread, recency)

## What This Agent Does NOT Do

- Does not verify factual correctness
- Does not evaluate source credibility
- Does not restrict collection to predefined publishers
- Does not interpret events or infer intent
- Does not generate opinions or analytical conclusions
- Does not autonomously trigger summaries or actions

## Output Behavior

When asked for a summary, the agent produces:

- One unified report
- Neutral, news-anchor style language
- Importance-ranked coverage
- Focus on *what happened*, not *why it happened*

## Intended Use Cases

- Feeding political intelligence systems
- Supporting fine-tuning and dataset creation
- Acting as an upstream signal source for RAG pipelines
- Providing raw, structured context for downstream analysis

## Project Status

This repository currently focuses on architectural clarity and system design.  
Implementation details are developed incrementally with an emphasis on correctness, simplicity, and extensibility.

---

Jarvis is the internal ingestion agent powering this system.

