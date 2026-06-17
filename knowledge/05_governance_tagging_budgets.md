# Cost Governance — tagging, budgets, monitoring, policies

**Questions this answers:** How do I attribute spend to teams/LOBs? How do I stop overspend before it happens? How do I enforce good cost behavior across many workspaces?

## Tag for cost attribution (do this first, it isn't retroactive)

- Tag workspaces, clusters, SQL warehouses, and pools so usage maps to business units and teams (for chargeback/showback). Tags propagate to usage logs, the `system.billing.usage` table, and cloud resources.
- Establish a tag naming convention org-wide. At minimum set custom tags **Business Unit** and **Project**; add **Environment** (dev/QA/prod) if you need to separate those costs.
- **Start tagging early and detailed** — tags only affect *future* usage; missing tags can't be backfilled. Over-tag rather than under-tag; you can ignore unused tags later.
- In our dashboard, the LOB → Sub-division → Team mapping is exactly this attribution layer (modeled as cost-center tags over workspaces).

## Budgets and alerts

- Use **Budgets** to set financial targets across the account, or filtered to specific teams/projects/workspaces.
- Configure **email alerts** when a monthly budget threshold is reached to avoid surprise overspend.
- For serverless, use **usage policies** to attribute serverless DBUs to users/groups/projects.

## Monitor with the right tools

- **Account cost dashboards** (AI/BI usage dashboards) — import into any UC-enabled workspace to monitor account- or workspace-level usage.
- **System tables** — `system.billing.usage` (+ serverless, jobs, and model-serving cost views) for custom analysis; tags flow through.
- **Regular cost audits** — review active resources vs need monthly; share reports to surface anomalies; educate teams on the cost impact of their choices.

## Enforce good behavior with compute policies

Compute policies are the durable control that prevents waste from recurring:

- Require **autoscaling** with a sensible minimum.
- Require **auto-termination** (e.g. ~1 hour) so nothing idles forever.
- Restrict to **cost-efficient, current-generation instance types**; block expensive ones (e.g. GPU) except where approved.
- Enforce a **spot strategy** for eligible workers.
- Define standardized **T-shirt-size** policies (Small/Medium/Large) so teams pick from safe presets instead of over-provisioning.

Treat cost optimization as an ongoing process — revisit policies on scaling, new projects, or cost spikes.

Source: Azure Databricks — *Best practices for cost optimization* (Monitor and control cost; compute policies) (learn.microsoft.com), 2026.
