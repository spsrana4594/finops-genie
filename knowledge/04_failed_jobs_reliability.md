# Failed-Job Cost & Reliability

**Questions this answers:** Why does a failed job still cost money? How do I stop paying for failed/retried runs? What causes most failures and how do I fix them?

## Why failed runs cost money

You pay for compute consumed up to the point a run fails — setup, execution, and any retries — regardless of whether the run produced useful output. A job that fails late (after heavy processing), or retries repeatedly, can burn significant DBUs for zero business value. High `failed_cost` or many `failed_runs` for a team is wasted spend *and* a reliability problem.

## How to reduce failed-job cost

1. **Fix the root cause, don't just retry.** Inspect `result_state` and `termination_code` for the failing runs. Common causes and fixes:
   - **OOM / executor lost** → increase instance memory (memory-optimized family), reduce per-task data, fix skew, or lower parallelism. See cluster sizing.
   - **Timeouts** → set realistic task timeouts; investigate slow stages/skew; right-size compute.
   - **Spill-then-fail on joins/aggregations** → fewer, larger memory-optimized workers; optimize the query and data layout.
   - **Dependency/credential/path errors** → fix config; fail fast rather than after expensive compute.
2. **Set sensible retry policies.** Unbounded or aggressive retries multiply cost. Cap retries and add backoff; alert when a job exceeds its retry budget instead of silently re-running.
3. **Fail fast / validate early.** Put cheap validation (schema, inputs, permissions) at the start so a doomed run stops before consuming expensive compute.
4. **Right-size and isolate.** Run jobs on job compute (not all-purpose), so a failed run's cluster tears down immediately instead of lingering idle.
5. **Monitor failure trends.** A job that fails every run is a standing cost leak — prioritize the highest `failed_cost` jobs first (the dashboard ranks them).

## Tie-in with the data

The dashboard's `failed_cost` = cost of runs that ended FAILED / ERROR / TIMED_OUT. Use the result-state and termination-code breakdowns to find the dominant failure mode per team, then apply the matching fix above.

Source: Azure Databricks system tables (`system.lakeflow.job_run_timeline`) + cost-optimization and compute-configuration best practices (learn.microsoft.com), 2026.
