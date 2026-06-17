# 💸 FinOps Genie

**Turn the Databricks system tables every workspace already has into actionable, team-tagged
cost-optimization recommendations** — an AI/BI dashboard + a curated Genie space, *recommendations first*.

![License](https://img.shields.io/badge/license-MIT-green)
![System tables](https://img.shields.io/badge/data-system.*%20tables-FF3621)
![No setup](https://img.shields.io/badge/setup-no%20objects%20created-00A972)
![Live](https://img.shields.io/badge/queries-100%25%20live-blue)

> Every query hits `system.*` **directly** — no pipelines, no exports, no materialized tables, no
> objects to create. The org breakdown (LOB / sub-division / team) comes from your `custom_tags`.

---

## ✨ What you get

| | |
|---|---|
| 📊 **FinOps Genie Dashboard** | 10 tabs — Overview (+ **team optimization leaderboard**), **To-Do / Optimization** (the headline), and per-compute-family consumption tabs |
| 🧞 **FinOps Genie** | Plain-English Q&A: *"What should the X team fix first?"*, *"Biggest savings by lever?"*, *"Which unused tables can we de-commission?"* |
| 📚 **Knowledge Assistant** (optional) | Blends best-practice how-to + your policy with the live data |

**🎯 The moat — the To-Do / Optimization tab:** every recommendation, **tagged to the owning team**,
dollarized, across three levers:

- 🔴 **Reduce waste** — idle clusters & warehouses, failing jobs, unused/zombie warehouses, over-frequent jobs, de-commission unused tables
- 🟠 **Rightsize infra** — oversized warehouses, VM/instance right-sizing, jobs-on-all-purpose, spot-with-fallback, autoscaling
- 🔵 **Optimize data & code** — query spill, long-running-query timeouts, runtime upgrades, predictive optimization *(deep tuning routes to Genie + Assistant)*

**🗂️ Consumption tabs:** All Purpose · Jobs · SQL Warehouses · AI/ML · Apps · Lakebase · Platform — each with **top teams / top products / top workspaces**. Plus a **Data** tab (table lifecycle).

---

## 🔌 Data sources (all `system.*`)

| System table | Powers |
|---|---|
| `system.billing.usage` + `list_prices` | Spend, cost, SKU & product breakdown |
| `system.access.workspaces_latest` | Workspace names |
| `system.compute.clusters` + `node_timeline` | Cluster CPU/mem utilization, idle cost, DBR, spot |
| `system.compute.warehouses` + `warehouse_events` | Warehouse idle cost, auto-stop |
| `system.query.history` | Query spill, long-running queries, top queries |
| `system.lakeflow.job_run_timeline` + `jobs` | Failed jobs, jobs-on-all-purpose, top jobs |
| `system.access.table_lineage` | Unused tables (Data tab) |
| `system.storage.predictive_optimization_operations_history` | Predictive-optimization coverage |

### Capabilities & limitations
- ✅ Actionable, **team-tagged** optimization recommendations (waste / rightsize / data)
- ✅ Per-compute-family consumption + top consumers, products & workspaces
- ✅ **Team optimization leaderboard** (efficiency score = `100 − all-lever savings / spend`)
- ✅ **Zero objects created** — pure live system tables; org from `custom_tags`
- 💰 Costs reflect **list prices** (`system.billing.list_prices`) unless `account_prices` is enabled
- ⚠️ On **very large accounts** (thousands of workspaces), the recommendation/leaderboard tiles run live and can be slow — see [Advanced](#-advanced-very-large-accounts)
- 🚫 No per-query cost attribution on shared compute (use Query History)

---

## ✅ Prerequisites

- A **SQL warehouse**
- **System tables enabled** ([docs](https://docs.databricks.com/admin/system-tables/)) for the schemas above — a tab whose schema isn't enabled simply comes up empty
- Databricks CLI configured (`databricks auth login`) — *only needed for the Genie import*
- 🏷️ **Optional (for the org breakdown):** tag resources with `custom_tags` keys `lob`, `sub_division`, `team`, `environment`. Untagged → shown as "Untagged"; everything else still works

---

## 🚀 Setup

```bash
git clone https://github.com/spsrana4594/finops-genie.git && cd finops-genie
```

**1️⃣ Dashboard** — in the workspace: **Dashboards → ⋮ → Import dashboard from file →**
`dashboard/finops_genie.lvdash.json` → pick a SQL warehouse → **Publish**.
*(CLI alternative: `python dashboard/import_dashboard.py --profile DEFAULT`)*

**2️⃣ Genie space** — no UI file-import exists for Genie, so use the script (recreates tables +
instructions + sample questions + example SQLs):
```bash
python genie/import_genie.py --profile DEFAULT
```

**3️⃣ Knowledge Assistant** *(optional)* — see [`knowledge/SETUP_KA.md`](knowledge/SETUP_KA.md).
The policy file [`knowledge/10_finops_policy_template.md`](knowledge/10_finops_policy_template.md)
is a **blank fill-in template** — drop in your own thresholds.

> Both scripts accept `--warehouse-id <id>` to pin a warehouse. That's it — open the dashboard and Genie.

---

## 🛠️ Customize

- **Tag keys** — derived in an `org` CTE at the top of each dataset (`custom_tags['lob']`, …); rename to your standard
- **Policy thresholds** — in the Genie instructions + `knowledge/10_finops_policy_template.md`
- **Savings assumptions** (spot ~30%, jobs-on-APC ~50%, …) — inline in the To-Do dataset SQL

---

## 🧩 How it works

Each dataset is a self-contained query over `system.*`: it prices `billing.usage` against
`list_prices`, derives the org from `custom_tags`, and computes waste / right-size / data signals
inline from `node_timeline` (cluster CPU), `warehouse_events` + `query.history` (idle / spill /
long-running queries), `job_run_timeline` (failed / all-purpose jobs), and `table_lineage` +
`storage` (unused tables / predictive optimization). The Genie space uses the same patterns as
curated example SQLs.

## 📁 Repo layout

```
dashboard/finops_genie.lvdash.json    AI/BI dashboard (pure system tables + custom_tags)
dashboard/import_dashboard.py         optional one-command import
genie/finops_genie.geniespace.json    Genie space (recommendations-first)
genie/import_genie.py                 Genie import (no UI file-import exists)
knowledge/                            10 best-practice guides + policy template + SETUP_KA.md
README.md · LICENSE · .gitignore
```

## 🐘 Advanced (very large accounts)

For accounts with thousands of workspaces where live tiles are too slow, precompute the heavy
datasets into tables on a schedule and point the dashboard at them. (Open an issue for the
precompute recipe.)

---

> ⚠️ **Not a Databricks product.** This is a **sample / community implementation** built on public
> Databricks system tables and APIs — provided as-is for demonstration. It is **not** an official
> Databricks offering and is not supported by Databricks. Review all dashboard and Genie outputs for
> accuracy before acting on them; recommendation savings are **estimates** based on configurable
> assumptions.

📄 **License:** MIT — see [LICENSE](LICENSE).
