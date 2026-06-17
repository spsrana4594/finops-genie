# SQL Warehouse Optimization — idle cost, sizing, scaling, spills

**Questions this answers:** How do I cut idle SQL warehouse cost? Serverless vs pro vs classic? How do I size a warehouse? When do I upsize vs add clusters? My queries are spilling — what do I do?

## Cut idle warehouse cost

A warehouse that is "running but not querying" is burning money. Fixes:

1. **Use serverless SQL warehouses.** They start and scale in seconds (vs minutes for pro/classic), so you can set aggressive idle termination and still get instant availability. They also scale *down* earlier than non-serverless. This is the most effective fix for idle cost and for the "users leave it on because cold start is slow" problem.
2. **Set a low auto-stop.** Classic/pro warehouses have minutes-long cold starts, so people leave them on. Lower the auto-stop aggressively (serverless makes this painless). A warehouse with auto-stop disabled (never stops) is the worst case — fix first.
3. **Consolidate under-used warehouses.** Many low-utilization warehouses → merge into fewer, right-sized, scaling ones.

## Serverless vs Pro vs Classic

- **Serverless** — recommended default. Instant elastic compute (no waiting, no over-provisioning), Intelligent Workload Management (IWM) for many concurrent queries, minimal management (patching/upgrades/tuning handled), lowest TCO via auto provision/scale and reduced idle. Photon always on.
- **Pro / Classic** — only when serverless isn't available/permitted; expect minute-scale starts and higher idle cost. Photon is on by default for all SQL warehouses.

## Sizing and scaling (two different knobs)

- **Warehouse size (t-shirt: 2X-Small … 4X-Large)** controls the power for a *single* query. Upsize when individual queries are slow or **spilling** (see below).
- **Clusters (min/max)** control *concurrency* — how many simultaneous queries/users the warehouse serves. Add clusters (raise max) when queries queue under concurrent load; don't upsize for that.
- Start at **Small or Medium with autoscaling** and adjust from observed behavior. Size by concurrent user count and query complexity.

## Spills and "potential upsizing" signals

A query that **spills to disk** ran out of memory for its working set and wrote intermediate data to local disk — slow and costly. When the dashboard flags spills:

1. **Upsize the warehouse** (more memory per query) — the direct fix for chronic spill.
2. **Optimize the query/data** — prune columns, filter early, fix skew, and ensure tables are well-laid-out (Delta, OPTIMIZE / liquid clustering) so less data is shuffled.
3. **Rely on Photon** (on by default) for vectorized execution; it especially helps joins, aggregations, and large scans.
4. Distinguish from **queuing** — if the problem is many concurrent queries rather than one heavy query, add clusters instead of upsizing.

Source: Azure Databricks — *Connect to a SQL warehouse*, *SQL warehouse types / sizing & scaling behavior*, and *Best practices for cost optimization* (learn.microsoft.com), 2026.
