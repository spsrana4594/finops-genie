# Databricks FinOps Optimization — Overview and How-To Index

This knowledge base lets the FinOps Genie agent answer the "how" and "why" questions that the dashboard's numbers can't: once a team sees its waste, *what should it actually do?* It is grounded in Databricks' official cost-optimization and compute-configuration best practices.

## How to use this with the dashboard

The dashboard surfaces *where* money is wasted (per team/workspace). This knowledge base explains *how to fix each category*:

| Dashboard signal / recommendation category | Where to find the fix |
|---|---|
| Underutilized compute (low avg CPU/memory on clusters) | `01_cluster_compute_optimization` |
| Which compute/VM type to use (e.g. for ephemeral jobs) | `01_cluster_compute_optimization` |
| Jobs running on all-purpose compute (anti-pattern) | `01_cluster_compute_optimization` (job vs all-purpose) |
| Idle SQL warehouses / warehouse idle cost | `02_sql_warehouse_optimization` |
| Query spills / warehouse upsizing | `02_sql_warehouse_optimization` |
| Outdated runtime (DBR versions behind) | `03_runtime_photon_spot_pools` |
| Spot adoption / startup time | `03_runtime_photon_spot_pools` |
| Failed-job cost | `04_failed_jobs_reliability` |
| Cost attribution, budgets, governance | `05_governance_tagging_budgets` |
| Always-on streaming, serverless choices, GPU misuse | `06_workload_design` |
| Data layout, OPTIMIZE/VACUUM, predictive optimization, liquid clustering | `07_data_layout_optimization` |
| Lakeflow / DLT pipeline cost (triggered, enhanced autoscaling, serverless) | `08_lakeflow_dlt_pipelines` |
| AI / ML & model-serving cost (scale-to-zero, provisioned vs pay-per-token, batch) | `09_ai_serving_cost` |
| Company-specific mandatory policy (Private Link, auto-stop, prod compute policies, tagging, efficiency targets) | `10_company_finops_standards` |

**Note:** `10_company_finops_standards` is the bank's *internal, bespoke* policy. Apply it when a user asks whether something is compliant or "what should it be" — judge the team's actual numbers against the company thresholds, and name the policy. This is knowledge the base model cannot have.

## The four principles of cost optimization (Databricks Well-Architected)

1. **Choose optimal resources** — performance-optimized formats (Delta), job compute for non-interactive work, SQL warehouses for SQL, up-to-date runtimes, Photon, the right instance family, and serverless where supported.
2. **Dynamically allocate resources** — autoscaling, auto-termination, instance pools, and compute policies so you pay only for what you use.
3. **Monitor and control cost** — tagging for attribution, budgets and alerts, system-table cost dashboards, regular audits.
4. **Design cost-effective workloads** — triggered vs always-on streaming, serverless for bursty BI/ML, GPUs only where they help.

## Answering style for the agent

- Be specific and actionable: name the setting (auto-termination minutes, autoscaling min/max, instance family, warehouse size, `AvailableNow` trigger) and the expected cost effect.
- When a team's data shows a problem (e.g. avg CPU 12%), tie the advice to that signal ("clusters averaging well under ~50% CPU are over-provisioned — reduce max workers or enable autoscaling from a lower minimum").
- Prefer serverless and job compute for the relevant workloads; explain the trade-off briefly.

Source: Azure Databricks — *Best practices for cost optimization* and *Compute configuration recommendations* (learn.microsoft.com), 2026.
