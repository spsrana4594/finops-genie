# Designing Cost-Effective Workloads

**Questions this answers:** Does my streaming pipeline need to run 24/7? When should I use serverless? When are GPUs worth it? How does data layout affect cost?

## Streaming: always-on vs triggered

- "Streaming" doesn't have to mean 24/7 compute. If the business only needs fresh data every few hours or daily, run incrementally instead of continuously.
- Use **Structured Streaming with the `AvailableNow` trigger** for incremental batch processing without low-latency requirements — process all new data, then stop, so compute isn't billed around the clock.
- For genuine low-latency streaming, use **Lakeflow Spark Declarative Pipelines with enhanced autoscaling** (classic autoscaling scales down poorly for streaming).

## Use serverless for bursty workloads

- **BI / dashboards** consume data in bursts with concurrent queries. Serverless SQL warehouses start in seconds and terminate when idle — instant availability *and* low idle cost. Non-serverless warehouses' slow starts push users to leave them on (expensive).
- **Model serving** loads vary over time; serverless **Model Serving** auto scales up/down to demand, minimizing infra cost while holding latency.

## GPUs only where they help

- GPU VMs dramatically speed deep learning but are far more expensive than CPU-only machines.
- Most workloads don't use GPU-accelerated libraries and gain nothing from GPUs. Use GPU instances only for GPU-accelerated ML/DL; have admins restrict GPU machines to prevent accidental/unnecessary use.

## Data formats and layout

- Use **Delta Lake** as the storage framework — simpler, more reliable pipelines and significant performance gains over Parquet/ORC/JSON. Faster jobs = shorter compute uptime = lower cost.
- Keep tables optimized (OPTIMIZE / liquid clustering, good partitioning) so queries scan and shuffle less — directly reducing both runtime and spill.

Source: Azure Databricks — *Best practices for cost optimization* (Design cost-effective workloads) (learn.microsoft.com), 2026.
