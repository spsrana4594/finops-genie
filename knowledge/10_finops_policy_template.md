# FinOps Policy — Template (fill this in)

This is a **blank template** for your organization's FinOps standard. The Genie space and Knowledge
Assistant use it to answer *"is this compliant?"* and *"what should it be?"* — but **the values below
are placeholders**. Replace every `<TODO>` with your own thresholds and process, then upload this
file to the Knowledge Assistant volume (see `SETUP_KA.md`). Nothing here is Databricks product
guidance.

> Until you fill these in, Genie will still answer cost/waste/optimization questions from the data —
> it just won't enforce specific compliance thresholds.

## 1. Network & security
- Connectivity: `<TODO — e.g. Private Link / no-public-IP only>`
- Serverless network security: `<TODO>`
- Unity Catalog / access mode requirement: `<TODO>`
- Data residency / approved regions: `<TODO>`
- Secrets handling: `<TODO>`

## 2. Compute settings
- Cluster auto-termination max (interactive / prod): `<TODO — e.g. N minutes>`; dev: `<TODO>`
- SQL warehouse auto-stop max: `<TODO — e.g. N minutes>`; never-auto-stop allowed? `<TODO: no>`
- Autoscaling requirement: `<TODO>`
- Spot-with-fallback policy (which workloads): `<TODO>`
- Photon requirement: `<TODO>`

## 3. Databricks Runtime
- Supported runtime window: `<TODO — e.g. within N LTS of latest>`
- Non-LTS in prod allowed? `<TODO>`

## 4. Compute policies by environment
- Production jobs must run on: `<TODO — e.g. job compute / serverless; all-purpose prohibited>`
- Production SQL must use: `<TODO>`
- Dev/personal limits: `<TODO>`
- GPU access: `<TODO>`

## 5. Tagging (mandatory)
- Required tags on every resource: `<TODO — e.g. cost_center, lob, sub_division, team, environment, app_id>`
  *(The dashboard's org breakdown reads these from `custom_tags`.)*

## 6. Data & storage
- Table format / managed vs external: `<TODO>`
- Predictive optimization requirement: `<TODO>`
- Clustering / layout standard: `<TODO>`
- Retention / VACUUM policy: `<TODO>`

## 7. AI / model serving
- Scale-to-zero requirement: `<TODO>`
- Provisioned vs pay-per-token: `<TODO>`
- Batch vs real-time: `<TODO>`

## 8. Efficiency targets & governance
- Team efficiency-score target: `<TODO — e.g. >= 80>`
- Waste budget (% of spend): `<TODO — e.g. <= 10%>`
- Budgets / alert thresholds: `<TODO>`
- Review cadence & owner: `<TODO — e.g. monthly FinOps council>`

## Compliance quick-reference (fill in your values)

| Signal in the data | Compliant if | Violation if |
|---|---|---|
| Cluster auto-stop (minutes) | `<TODO>` | `<TODO>` |
| Warehouse never-auto-stop / auto-stop | `<TODO>` | `<TODO>` |
| Spot on eligible batch workers | `<TODO>` | `<TODO>` |
| Runtime versions behind | `<TODO>` | `<TODO>` |
| Scheduled jobs on all-purpose compute | `<TODO>` | `<TODO>` |
| Team efficiency score | `<TODO>` | `<TODO>` |
| Waste / spend | `<TODO>` | `<TODO>` |
