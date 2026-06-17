#!/usr/bin/env python3
"""
Import the FinOps Genie space into your workspace.

Pure system tables — nothing to create. Creates the Genie space from
genie/finops_genie.geniespace.json and binds it to a SQL warehouse.
Works on any Databricks CLI version (uses the REST API directly).

Usage:
  python genie/import_genie.py --profile DEFAULT [--warehouse-id <id>] [--parent-path /Users/you@example.com]

If --warehouse-id is omitted, the first available SQL warehouse is used.
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
    ap.add_argument("--parent-path", default=None, help="Workspace folder; defaults to your home")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    serialized = open(os.path.join(here, "finops_genie.geniespace.json")).read()

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

    out = api("POST", "/api/2.0/genie/spaces", args.profile, {
        "title": "FinOps Genie",
        "description": "Cost, waste, efficiency and optimization Q&A over Databricks system tables.",
        "warehouse_id": wh, "parent_path": parent, "serialized_space": serialized,
    })
    print("Created Genie space:", out.get("space_id"))
    print("Open it from the Genie section of your workspace.")

if __name__ == "__main__":
    main()
