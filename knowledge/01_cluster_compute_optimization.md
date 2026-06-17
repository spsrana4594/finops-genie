# Cluster & Compute Optimization — reduce underutilization, pick the right compute

**Questions this answers:** How do I bring cluster underutilization (low CPU/memory) down? Which VM/instance type should I use for ephemeral jobs, interactive analysis, streaming, or ML? Should this run on job compute or all-purpose compute? Fewer large nodes or more small nodes? When to use spot? How do I cut cluster startup time?

## Reducing cluster underutilization (low avg CPU / memory)

Clusters that average well below ~50% CPU (or low memory use) are over-provisioned — you are paying for cores that sit idle. Actions, in order of impact:

1. **Enable autoscaling and lower the minimum.** Databricks dynamically adds/removes workers to match the job. Set a small minimum (e.g. 1–2 workers) and a max that covers peaks. This is the single biggest lever for variable workloads.
2. **Reduce max workers / instance size.** If utilization is consistently low even at minimum, the cluster is simply too big. Right-size down. Remember: 2 workers × 16 cores = 8 workers × 4 cores in total compute — choose the shape that fits the workload (see node-count trade-off below).
3. **Enable auto-termination.** Configure auto-termination on every interactive cluster (e.g. ~60 minutes idle, lower for dev). Idle clusters that never stop are pure waste.
4. **Use serverless where supported** (notebooks, jobs, Lakeflow pipelines). Serverless removes the sizing decision entirely, is always available, and scales to the workload — the simplest way to eliminate idle.
5. **Move scheduled work off interactive clusters** (see job vs all-purpose below).
6. **Use compute policies** to cap instance types and max workers and *require* autoscaling + auto-termination, so under-utilization can't recur.

## Choosing the instance/VM family (rules of thumb)

- **Memory optimized** — ML, heavy shuffle, and spill-heavy workloads (joins/aggregations that spill to disk).
- **Compute optimized** — structured streaming and maintenance jobs (OPTIMIZE, VACUUM).
- **Storage optimized** (with disk cache) — ad-hoc/interactive analysis that re-reads the same data.
- **GPU optimized** — only for GPU-accelerated ML/DL libraries (GPUs are far more expensive; don't use them for non-GPU work).
- **General purpose** — when there's no specific requirement.
- Prefer the **latest instance generation** — newer VMs almost always give a better performance/price ratio.

## Which compute for ephemeral jobs?

Ephemeral (scheduled, non-interactive) jobs should run on **job compute** (or **serverless jobs**), never on a long-lived all-purpose cluster:

- **Job compute** spins up for the run and tears down after — you pay only for the run, at the cheaper Jobs DBU rate.
- **Serverless jobs** are simplest: no sizing, fast start, scale to the work, no idle.
- Instance family for the job: **basic batch ETL** (no wide joins) → lower-memory/lower-storage instances to save cost; **complex ETL** (joins/unions, spill or OOM observed) → fewer, larger, memory-optimized instances; **streaming** → compute optimized.
- For multitask jobs, tasks can share one compute so startup happens once per job.

## Job compute vs all-purpose compute (a common, costly anti-pattern)

Running scheduled jobs on **all-purpose** compute costs significantly more than **job** compute for the same work (compare Jobs vs All-Purpose DBU pricing). All-purpose is for interactive notebook use; jobs should use job compute or serverless jobs. Moving jobs off all-purpose typically cuts their DBU cost by roughly half and isolates workloads from each other.

## Fewer large nodes vs more small nodes

- **Complex ETL with joins/aggregations / heavy shuffle** → *fewer, larger* workers reduce network + disk I/O from shuffles; increase instance memory if you see spill or OOM.
- **Data analysis (single analyst)** → a single-node large VM is often best; storage-optimized with disk cache for repeated reads.
- **Basic batch ETL (no wide transforms)** → smaller, cheaper instances.
- Sizing factors that matter more than worker count: total executor cores (parallelism), total executor memory (spill threshold), and local storage (shuffle/cache).

## Spot instances

Use spot/excess-capacity instances for the workers to save cost on workloads that tolerate occasional eviction (jobs that can take longer if a node is reclaimed). Keep the **driver on an on-demand instance** for stability. Apply a spot strategy via compute policies.

## Cluster startup time (instance pools)

If startup time pushes teams to leave clusters running (causing idle waste), use **instance pools** — a set of idle, ready-to-use instances that cut cluster start and autoscale times. Databricks does not charge DBUs for idle pooled instances (cloud VM charges still apply), so pools reduce both startup latency and the temptation to never auto-terminate.

Source: Azure Databricks — *Compute configuration recommendations* and *Best practices for cost optimization* (learn.microsoft.com), 2026.
