# Lakeflow / DLT Pipeline Cost Optimization

**Questions this answers:** How do I make my Lakeflow Spark Declarative Pipelines (DLT) cheaper? Continuous vs triggered pipelines? How should pipelines autoscale?

## Triggered vs continuous

- **Triggered** pipelines run, process available data, and stop — you pay only while processing. **Continuous** pipelines keep compute running 24/7.
- Default to **triggered** unless the use case truly needs low-latency continuous updates. If freshness of hours/daily is acceptable, triggered (or Structured Streaming with the `AvailableNow` trigger) dramatically cuts cost versus always-on.

## Enhanced autoscaling

- Use Lakeflow pipelines' **enhanced autoscaling** for streaming/continuous workloads. Classic cluster autoscaling scales *down* poorly for streaming; enhanced autoscaling is designed to release idle resources for streaming, lowering cost while protecting latency.

## Serverless pipelines

- Prefer **serverless** for Lakeflow pipelines where supported: no cluster sizing, fast start, scale-to-workload, and no idle compute between triggered runs. This removes the most common pipeline waste (over-sized or idling pipeline clusters).

## Photon and runtime

- Pipelines with wide transformations (joins/aggregations) benefit from Photon. Keep pipelines on current runtimes for free performance gains (shorter run = lower cost).

## Data layout

- Land pipeline outputs as **Delta managed tables** with **predictive optimization** and **liquid clustering** enabled so downstream reads scan less data (see `07_data_layout_optimization`). This compounds savings across every consumer of the pipeline's tables.

## Practical guidance for the agent

- If a pipeline's cost is high and latency needs are loose, recommend triggered execution / `AvailableNow` and serverless.
- If a continuous pipeline shows low utilization, recommend enhanced autoscaling and a lower minimum.

Source: Azure Databricks — *Best practices for cost optimization* (Design cost-effective workloads; auto-scaling) and Lakeflow Spark Declarative Pipelines docs (learn.microsoft.com), 2026.
