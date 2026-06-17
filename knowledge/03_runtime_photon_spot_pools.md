# Runtime versions, Photon, Spot, and Pools

**Questions this answers:** My clusters are several DBR versions behind — why upgrade and how? When should I turn on Photon? How do spot instances and instance pools save money?

## Keep Databricks Runtime (DBR) up to date

- DBR releases come on a regular cadence with performance improvements between major releases. Faster execution = shorter compute uptime = lower cost, often with no code change.
- Standardize on the **latest LTS** (long-term support) release for production; LTS gives the stability/support window plus the performance gains.
- "Versions behind" on the dashboard is a hygiene signal: clusters many majors behind are leaving both performance and money on the table. Plan upgrades, test on the new LTS, and roll forward.
- Use **Databricks Runtime for ML** for ML workloads (curated, compatible library set) rather than installing everything manually.

## Photon — when to turn it on

Photon is Databricks' native vectorized engine; compatible with Spark APIs, so it's just a toggle — no code change, no lock-in.

- **Most beneficial for:** SQL workloads and DataFrame operations with complex transformations (joins, aggregations, large scans), wide tables, frequent disk access, or repeated processing.
- **Minimal benefit for:** simple batch ETL with no wide transformations / small data / sub-2-second queries.
- It's **on by default for all SQL warehouses.** For jobs/clusters, evaluate regularly-run jobs: if Photon makes them faster *and* cheaper (shorter uptime outweighs the Photon DBU multiplier), enable it.

## Spot instances

- Use spot (excess-capacity) instances for **workers** to cut cost on workloads that tolerate occasional eviction (a run may take longer if a node is reclaimed).
- Keep the **driver on-demand** for stability ("spot with fallback to on-demand" pattern).
- Enforce via compute policies so teams adopt spot consistently. Low spot adoption on expensive, eviction-tolerant batch jobs is an easy saving.

## Instance pools (startup time → fewer idle clusters)

- Pools keep a set of idle, ready instances so cluster **start and autoscale times** drop.
- Databricks charges **no DBUs** for idle instances sitting in a pool (cloud VM charges still apply).
- Why it saves money: when startup is slow, teams disable auto-termination and leave clusters running. Pools make starts fast, so teams can safely auto-terminate — removing idle waste. Restrict pools to pre-approved, cost-efficient instance types.

Source: Azure Databricks — *Compute configuration recommendations*, *Best practices for cost optimization*, *Photon* (learn.microsoft.com), 2026.
