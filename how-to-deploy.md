# 🚀 How to Deploy Prefect Flows

## ✅ Prerequisites

- 🐍 Python 3.12 installed on Windows
- 📦 Prefect 3.6.1 installed: `pip install prefect==3.6.1`  
- 🐳 Docker containers running (prefect-server and prefect-worker)

## 🗂 Deploying with `prefect.yaml`

Using the repo's `prefect.yaml` keeps deployment settings (entrypoint, pull steps, work pool, tags, etc.) under version control. The CLI will read this file automatically from the project root.

1. **Point the CLI at your server (per terminal session):**
	```bash
	export PREFECT_API_URL=http://localhost:4200/api
	```
2. **Apply a deployment from the manifest:**
	```bash
	cd /e/prefect-demo
	prefect deploy -n cedar7-cost-by-eq
	```
	- `-n cedar7-cost-by-eq` matches the deployment name defined under `deployments` in `prefect.yaml`.
	- The command runs non-interactively and reuses the pull steps / work pool declared in the file.
3. **Add or modify deployments:** edit `prefect.yaml`, commit the changes, then rerun `prefect deploy -n <name>` (or omit `-n` to deploy all entries).
4. **Kick off a run after deploying:**
	```bash
	prefect deployment run 'cedar7-cost-by-eq/cedar7-cost-by-eq'
	```

Use this flow whenever you tweak flow code or infrastructure settings—no need to retype long CLI options each time.

## ⚡ Quick Start (prefect.yaml workflow)

1. **Set the Prefect API URL (per terminal session)**
	 ```bash
	 export PREFECT_API_URL=http://localhost:4200/api
	 ```
2. **Navigate to the repo root**
	 ```bash
	 cd /e/prefect-demo
	 ```
3. **Deploy the `cedar7-cost-by-eq` flow from `prefect.yaml`**
	 ```bash
	 prefect deploy -n cedar7-cost-by-eq
	 ```
	 The CLI reads `prefect.yaml`, applies the `cedar7-cost-by-eq` entry, and reuses its pull steps, work pool, and tags.
4. **Run the deployment**
	 ```bash
	 prefect deployment run 'cedar7-cost-by-eq/cedar7-cost-by-eq'
	 ```

Repeat steps 1–4 whenever you change flow code or update deployment metadata.

## ➕ Adding More Deployments to `prefect.yaml`

Add additional entries under the `deployments:` list. Example showing both cedar7 and a `chula-person-extraction` deployment:

```yaml
deployments:
  - name: cedar7-cost-by-eq
    entrypoint: flows/cedar7_cost_by_eq/flow_cedar7_cost_by_eq.py:sync_cost_by_eq
    pull:
      - prefect.deployments.steps.set_working_directory:
          directory: /app
    work_pool:
      name: cedar7-pool
      job_variables:
        working_dir: /app

  - name: chula-person-extraction
    description: Extract Person rows from SQL Server into JSON
    entrypoint: flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data
    parameters:
      table_name: Person
      output_filename: Person.json
      limit: 1000
    pull:
      - prefect.deployments.steps.set_working_directory:
          directory: /app
    work_pool:
      name: cedar7-pool
      job_variables:
        working_dir: /app
```

Deploy either entry by name:

```bash
prefect deploy -n cedar7-cost-by-eq
prefect deploy -n chula-person-extraction
```

Deploy everything in the file at once:

```bash
prefect deploy
```

After deploying, trigger the run you need:

```bash
prefect deployment run 'chula-person-extraction/chula-person-extraction'
```

## ▶️ Monitoring & Managing Deployments

- View deployments in the UI: `http://localhost:4200/deployments`
- Inspect via CLI: `prefect deployment inspect 'cedar7-cost-by-eq/cedar7-cost-by-eq'`
- Delete if needed: `prefect deployment delete 'chula-person-extraction/chula-person-extraction'`

## ⚙️ Parameters Reference

- `table_name` 👉 SQL Server table name to extract (required)  
- `output_filename` 👉 Output file name (default: `{table_name}.json`)  
- `limit` 👉 Number of rows to extract (default: 1000)

## 📂 Output Location

Extracted files are saved to `/app/output/` inside the Docker container,  
which is mounted to `./output/` in your workspace.

Example Windows path: `E:\prefect-demo\output\Person.json`

## 🔄 Updating Flow Code

1. ✏️ Edit files in `E:\prefect-demo\flows\chula_extraction\`  
2. ⚡ Changes take effect immediately (no rebuild needed)  
3. ▶️ Run the deployment – it uses the latest code

## 🧰 Troubleshooting

### 🔍 Check work pool status

```bash
export PREFECT_API_URL=http://localhost:4200/api
prefect work-pool ls
```

### 📋 View deployment details

```bash
export PREFECT_API_URL=http://localhost:4200/api
prefect deployment ls
```

### 🗑 Delete a deployment

```bash
export PREFECT_API_URL=http://localhost:4200/api
prefect deployment delete 'chula-person-extraction/chula-person-extraction'
```
