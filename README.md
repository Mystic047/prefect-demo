# Prefect Deployment Guide

Use this repo when you already have the flows and `prefect.yaml` checked in and only need to redeploy them with the Prefect CLI.

## Requirements

- Windows host with Docker running the Prefect API (start with `docker-compose up -d`).
- Python 3.12 installed and on PATH.
- Prefect 3.6.1 installed: `pip install prefect==3.6.1`.
- Access to this repository with `prefect.yaml` in the root directory.

## Deploying from `prefect.yaml`

Every deployment is declared in `prefect.yaml`, so redeploying is just a CLI command.

```bash
export PREFECT_API_URL=http://localhost:4200/api
cd /e/prefect-demo

# Deploy a single entry by name
prefect deploy -n cedar7-cost-by-eq

# Trigger the run right after
prefect deployment run 'cedar7-cost-by-eq/cedar7-cost-by-eq'

# Deploy another entry
prefect deploy -n chula-person-extraction
prefect deployment run 'chula-person-extraction/chula-person-extraction'

# Redeploy everything in the manifest (optional)
prefect deploy
```

Tips:

- Run `prefect deploy -n <name>` whenever you change flow code or metadata for that entry.
- Omit `-n` when you want to apply every deployment defined in the manifest.
- After editing `prefect.yaml`, commit the change so teammates inherit the same settings.

## Updating Deployments

1. Edit the relevant block under `deployments:` in `prefect.yaml` (entrypoint, parameters, pull steps, work pool, etc.).
2. Save and commit the file.
3. Rerun `prefect deploy -n <name>` to publish the changes.
4. Start a run with `prefect deployment run '<name>/<name>'` to verify.

That’s it—everything else (folder structure, troubleshooting, architecture) lives in the repo and can be referenced as needed.
