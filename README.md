# FinOps Genie

Open-source FinOps on Databricks: an **AI/BI dashboard** and a curated **Genie space** that turn the
**system tables every workspace already has** into **actionable, team-tagged cost-optimization
recommendations** — plus an optional **Knowledge Assistant** for the how-to.

Every query hits `system.*` **directly**. No pipelines, no exports, no materialized tables, no
objects to create. The org breakdown (LOB / sub-division / team) comes from your `custom_tags`.

> Less information overload, more automated, actionable optimization — recommendations first.

## What you get

- **FinOps Genie Dashboard** — 10 tabs:
  - **Overview** — spend, waste, efficiency, DBU, utilization KPIs + a **team optimization leaderboard** (efficiency score = `100 − all-lever savings / spend`, reflecting waste + rightsize + data).
  - **To-Do / Optimization** — the headline: every recommendation, **tagged to the owning team**, dollarized, across three levers (**Reduce waste · Rightsize infra · Optimize data & code**). ~14 rule types incl. idle clusters/warehouses, failing jobs, unused/zombie warehouses, over-frequent jobs, VM right-sizing, no-spot, autoscaling, **query-timeout**, and data recs (de-commission unused tables, enable predictive optimization).
  - **All Purpose · Jobs · SQL Warehouses · AI/ML · Apps · Lakebase · Platform** — per-compute-family consumption: spend + **top teams / top products / top workspaces**.
  - **Data** — table lifecycle: unused tables, predictive-optimization coverage, de-commission candidates.
- **FinOps Genie** — ask in plain English: *"What should the X team fix first?"*, *"Biggest savings by lever?"*, *"Which warehouses violate our auto-stop policy?"*, *"Which unused tables can we de-commission?"*
- **Knowledge Assistant** (optional) — blends best-practice how-to + your policy with the live data.

## Prerequisites

- A **SQL warehouse**.
- **System tables enabled** (one-time, by a metastore admin — see
  [docs](https://docs.databricks.com/admin/system-tables/)). Used: `system.billing` (usage,
  list_prices), `system.compute` (clusters, node_timeline, warehouses, warehouse_events),
  `system.lakeflow` (job_run_timeline, jobs), `system.query.history`, `system.access`
  (workspaces_latest, table_lineage), `system.storage`. A tab whose schema isn't enabled simply
  comes up empty rather than erroring.
- Databricks CLI configured (`databricks auth login`). *(Or use the UI import — see below.)*
- **Optional, for the org breakdown:** tag your resources with `custom_tags` keys `lob`,
  `sub_division`, `team`, `environment`. Untagged resources show as "Untagged" — everything else
  still works.

## Setup

```bash
git clone https://github.com/<you>/finops-genie.git && cd finops-genie
```

**1. Dashboard** — easiest is the UI: **Dashboards → (kebab menu) → Import dashboard from file →**
`dashboard/finops_genie.lvdash.json`, then pick a SQL warehouse and **Publish**.
*(Optional CLI alternative: `python dashboard/import_dashboard.py --profile DEFAULT`.)*

**2. Genie space** — there is no UI file-import for Genie spaces, so use the script (it recreates
the tables + instructions + sample questions + example SQLs for you):
```bash
python genie/import_genie.py --profile DEFAULT
```

**3. (optional) Knowledge Assistant** — adds best-practice how-to + your policy. See
[`knowledge/SETUP_KA.md`](knowledge/SETUP_KA.md). The policy file
(`knowledge/10_finops_policy_template.md`) is a **blank fill-in template** — drop in your own
thresholds; Genie works without it (just won't enforce specific compliance values).

Both scripts take `--warehouse-id <id>` to pin a warehouse (otherwise the first available is used).
That's it — open the dashboard and the Genie space.

> **Performance note:** queries run **live** against system tables. On a typical account (tens of
> workspaces) tabs load in seconds. On very large accounts (thousands of workspaces) the
> recommendation/leaderboard tiles are heavy and can take a while — bind to a larger warehouse, or
> see *Advanced* below.

## Customize

- **Tag keys:** the org is derived in an `org` CTE at the top of each dataset
  (`custom_tags['lob']`, etc.). Rename the keys there to match your tagging standard.
- **Policy thresholds** (auto-stop limits, efficiency target, DBR standard, etc.) live in the Genie
  instructions and in `knowledge/10_finops_policy_template.md` — edit to your standard.
- **Savings assumptions** (e.g. spot ~30%, jobs-on-APC ~50%) are inline in the To-Do dataset SQL.

## Repo layout

```
dashboard/finops_genie.lvdash.json   AI/BI dashboard (pure system tables + custom_tags)
dashboard/import_dashboard.py        one-command import
genie/finops_genie.geniespace.json   Genie space (system tables, recommendations-first)
genie/import_genie.py                one-command import
knowledge/                           10 best-practice guides + example policy + SETUP_KA.md
README.md  ·  LICENSE
```

## How it works (no magic)

Each dataset is a self-contained query over `system.*`: it prices `system.billing.usage` against
`system.billing.list_prices`, derives the org from `custom_tags`, and computes waste / right-size /
data signals inline from `system.compute.node_timeline` (cluster CPU), `warehouse_events` +
`query.history` (warehouse idle / spill / long-running queries), `system.lakeflow.job_run_timeline`
(failed / all-purpose jobs), and `system.access.table_lineage` + `system.storage` (unused tables /
predictive optimization). The Genie space uses the same patterns as curated example SQLs.

## Advanced (very large accounts)

For accounts with thousands of workspaces where live tiles are too slow, you can precompute the
heavy datasets into tables on a schedule and point the dashboard at them. (Ask in Issues / see the
talk materials for the precompute recipe.)

## License

MIT — see [LICENSE](LICENSE). Uses only Databricks system tables and public APIs. The included
policy is an editable example, not Databricks product guidance.
