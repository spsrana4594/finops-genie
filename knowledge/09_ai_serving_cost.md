# AI / ML & Model Serving Cost Optimization

**Questions this answers:** My AI/ML spend (model serving, vector search, foundation models) is high — how do I bring it down? Provisioned throughput vs pay-per-token? How do I avoid paying for idle endpoints?

(AI/ML is often a large and fast-growing spend bucket, so it deserves the same scrutiny as classic compute.)

## Serve on serverless and scale to zero

- **Model Serving** uses serverless compute and automatically scales up and down with request load, so you provision capacity only as needed. This is the default cost-efficient way to serve models.
- Enable **scale-to-zero** for endpoints that see intermittent traffic, so an idle endpoint stops incurring compute. Accept a small cold-start on the first request after idle. Don't run always-on endpoints for bursty/low-traffic models.
- Right-size endpoint **concurrency / compute size** to actual peak load rather than a generous guess; let autoscaling handle spikes.

## Provisioned throughput vs pay-per-token (foundation models)

- **Pay-per-token** (per-request billing) suits spiky, low-or-variable volume and experimentation — you pay only for tokens used.
- **Provisioned throughput** suits steady, high-volume production traffic where reserved capacity is cheaper per token and gives predictable latency.
- Match the mode to the traffic profile; using provisioned throughput for a low-traffic endpoint wastes reserved capacity, and pay-per-token for very high steady volume can cost more.

## Batch vs real-time

- For inference that doesn't need real-time responses, use **batch inference** (e.g. `ai_query` over a table on job/serverless compute) instead of a standing real-time endpoint — far cheaper for large offline scoring.

## GPUs only where they help

- Use GPU serving/training only for genuinely GPU-accelerated models; GPUs are far more expensive than CPU. Restrict GPU instances via policy to prevent accidental use (see `01_cluster_compute_optimization`).

## Vector Search and supporting services

- Size Vector Search endpoints to the index/query load; consolidate small indexes where possible and remove unused endpoints/indexes (idle endpoints still cost).

## Practical guidance for the agent

- High model-serving cost with bursty traffic → enable scale-to-zero and right-size concurrency.
- High steady foundation-model token cost → evaluate provisioned throughput vs pay-per-token.
- Large offline scoring on a real-time endpoint → move to batch inference.

Source: Azure Databricks — *Best practices for cost optimization* (serverless model serving; GPUs only for the right workloads) and Mosaic AI Model Serving docs (learn.microsoft.com), 2026.
