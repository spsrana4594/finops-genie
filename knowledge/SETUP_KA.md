# Setting up the Knowledge Assistant (optional)

The Genie space works fully on its own — it answers cost/waste/efficiency/policy
questions from your system tables. This optional **Knowledge Assistant (KA)** adds the
*"how do I actually fix this?"* layer: it reads the best-practice guides in this
`knowledge/` folder and the example policy, so Genie can synthesize **structured data
(SQL)** + **unstructured guidance (docs)** in one answer (e.g. "Team X is wasting $Y on
idle warehouses — here's the step-by-step remediation and the policy it violates").

> There is no public API to create a Knowledge Assistant today, so this is a short
> manual, one-time setup in the UI. ~5 minutes.

## 1. Upload the knowledge docs to a UC Volume
```sql
CREATE VOLUME IF NOT EXISTS main.finops.finops_knowledge_base;
```
Then upload every `.md` file in this `knowledge/` folder to
`/Volumes/main/finops/finops_knowledge_base/` (Catalog Explorer → the volume → Upload,
or `databricks fs cp knowledge/*.md dbfs:/Volumes/main/finops/finops_knowledge_base/`).
Replace `main.finops` with your catalog/schema.

## 2. Create the Knowledge Assistant
1. In the workspace, go to **Agents → Knowledge Assistant → Create**.
2. **Name:** `finops-optimization-advisor`.
3. **Description / instructions:** "Databricks FinOps optimization and policy advisor.
   Answer how to reduce cost and waste (idle compute, idle warehouses, failed jobs,
   runtime upgrades, Photon, spot, serverless, tagging) and how to comply with the
   FinOps policy. Be specific and actionable; cite the relevant guide."
4. **Knowledge source:** add the UC Volume from step 1 (all the `.md` files).
5. Create and wait for indexing to finish.

## 3. Link the Knowledge Assistant to the Genie space
1. Open the **FinOps Genie** space → **Settings / Instructions**.
2. Under **Knowledge / Assistants** (Genie + Knowledge Assistant integration), add
   `finops-optimization-advisor`.
3. Ensure **Agent mode** is enabled so Genie can call the assistant and blend its
   guidance with the SQL results.

## 4. Test
Ask the Genie space: *"Team X is below the efficiency target — what should they fix and
what does the policy require?"* You should get the dollarized data (from the views) plus
the how-to and the policy threshold (from the KA + the example policy doc).

If the KA is not configured, the same question still returns the data and the policy
values embedded in the Genie instructions — you just lose the long-form how-to.
