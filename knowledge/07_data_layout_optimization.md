# Data Layout Optimization — OPTIMIZE, Predictive Optimization, Liquid Clustering, VACUUM

**Questions this answers:** How does data layout affect cost? How do I stop manually running OPTIMIZE/VACUUM? Should I use partitioning, ZORDER, or liquid clustering? How do I reduce data scanned (and therefore compute) per query?

Why this matters for FinOps: poorly laid-out tables make every query scan and shuffle more data, inflating cluster/warehouse runtime, spills, and cost. Good layout is a *compounding* saving across all downstream workloads.

## Predictive Optimization (let Databricks do maintenance for you)

For Unity Catalog **managed** tables, predictive optimization automatically runs maintenance so teams don't have to:
- **OPTIMIZE** — compacts small files / incrementally clusters for better file sizes and query performance.
- **VACUUM** — deletes unreferenced data files, **reducing storage cost** (default retention 7 days via `delta.deletedFileRetentionDuration`; raise it before enabling if you need longer time travel).
- **ANALYZE** — keeps statistics current for better query plans.
- It only runs operations it predicts are worthwhile, removing wasted manual maintenance runs.
- Enabled by default for accounts created on/after 2024-11-11; gradual rollout to older accounts (through ~Aug 2026). Enable per account/catalog/schema: `ALTER CATALOG c ENABLE PREDICTIVE OPTIMIZATION;`
- Runs on **serverless jobs** compute (billed at the serverless jobs SKU) — track it via `system.storage.predictive_optimization_operations_history`.
- Recommendation: enable predictive optimization for all UC managed tables and **disable any scheduled OPTIMIZE jobs** (they become redundant and just cost money).

## Liquid Clustering (replaces partitioning + ZORDER)

Liquid clustering organizes data by clustering keys to maximize **data skipping**, so queries scan less and run cheaper. Use it for new tables instead of partitioning/ZORDER.
- **When it especially helps:** high-cardinality filter columns, skewed data, fast-growing tables, concurrent writes, changing/varied access patterns, and cases where a partition key returns too many/too few partitions.
- **Enable:** `CREATE TABLE t (...) CLUSTER BY (col)` or `ALTER TABLE t CLUSTER BY (col1, col2)` (up to 4 keys; pick the most frequent filter columns; keys must have statistics, i.e. within the first 32 columns by default).
- **Automatic liquid clustering** (DBR 15.4 LTS+, requires predictive optimization): `CLUSTER BY AUTO` lets Databricks pick and adapt clustering keys from the query workload, and it only changes keys when predicted data-skipping savings outweigh the clustering cost — fully cost-aware.
- **Reclustering:** `OPTIMIZE t` clusters incrementally (fast); `OPTIMIZE t FULL` reclusters everything (use when first enabling or after changing keys). With predictive optimization on, OPTIMIZE runs automatically.
- **Migrating:** use former partition columns and/or `ZORDER BY` columns as the clustering keys.

## Practical guidance for the agent

- If a team has heavy query spills or slow scans, recommend liquid clustering on the hot filter columns (or `CLUSTER BY AUTO`) plus predictive optimization — this reduces scanned data and shuffle, cutting both warehouse spills and cluster runtime.
- If a team runs manual nightly OPTIMIZE/VACUUM jobs, recommend enabling predictive optimization and retiring those jobs.
- Always pair good layout with up-to-date DBR + Photon for the largest effect.

Source: Azure Databricks — *Predictive optimization for Unity Catalog managed tables* and *Use liquid clustering for tables* (learn.microsoft.com), 2026.
