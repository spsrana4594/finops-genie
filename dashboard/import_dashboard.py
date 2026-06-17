#!/usr/bin/env python3
"""
Import the FinOps Genie Dashboard into your workspace.

Creates the AI/BI dashboard from dashboard/finops_genie.lvdash.json, binds it to a
SQL warehouse, and publishes it. Pure system tables — nothing else to create.

Usage:
  python dashboard/import_dashboard.py --profile DEFAULT [--warehouse-id <id>] [--parent-path /Users/you@example.com]

(Alternatively: in the workspace, Dashboards -> kebab menu -> Import dashboard from file,
 then pick a warehouse and Publish.)
"""
import argparse, json, os, subprocess, sys

def api(method, path, profile, body=None):
    cmd = ["databricks", "api", method, path, "--profile", profile]
    if body is not None:
        cmd += ["--json", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit(f"API {method} {path} failed: {r.stderr.strip() or r.stdout.strip()}")
    return json.loads(r.stdout)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="DEFAULT")
    ap.add_argument("--warehouse-id", default=None)
    ap.add_argument("--parent-path", default=None)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    serialized = open(os.path.join(here, "finops_genie.lvdash.json")).read()

    wh = args.warehouse_id
    if not wh:
        whs = api("GET", "/api/2.0/sql/warehouses", args.profile).get("warehouses", [])
        if not whs:
            sys.exit("No SQL warehouse found; pass --warehouse-id.")
        wh = whs[0]["id"]
        print(f"Using warehouse {whs[0].get('name')} ({wh})")

    parent = args.parent_path
    if not parent:
        me = api("GET", "/api/2.0/preview/scim/v2/Me", args.profile)
        parent = f"/Users/{me['userName']}"

    out = api("POST", "/api/2.0/lakeview/dashboards", args.profile, {
        "display_name": "FinOps Genie Dashboard",
        "serialized_dashboard": serialized,
        "parent_path": parent, "warehouse_id": wh,
    })
    did = out.get("dashboard_id")
    api("POST", f"/api/2.0/lakeview/dashboards/{did}/published", args.profile,
        {"warehouse_id": wh, "embed_credentials": True})
    print("Created + published dashboard:", did)

if __name__ == "__main__":
    main()
