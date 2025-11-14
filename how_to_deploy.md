# 🚀 How to Deploy Prefect Flows

## ✅ Prerequisites

- 🐍 Python 3.12 installed on Windows
- 📦 Prefect 3.6.1 installed: `pip install prefect==3.6.1`  
- 🐳 Docker containers running (prefect-server and prefect-worker)

## ⚡ Quick Start

### 1️⃣ Set Prefect API URL (once per terminal session)
put this command into the terminal (Git Bash or CMD)
==============================================
export PREFECT_API_URL=http://localhost:4200/api
==============================================

### 2️⃣ Deploy a Flow

Basic deployment (manual trigger only):

put this command into the terminal (Git Bash or CMD)
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name person-extraction \
	--pool chula-pool \
	--params '{"table_name":"Person","output_filename":"Person.json","limit":1000}'
=====================================================================================

## 📤 Deployment Options

### 🕹 Manual Trigger (No Schedule)

put this command into the terminal (Git Bash or CMD)
==============================================
export PREFECT_API_URL=http://localhost:4200/api
==============================================

put this command into the terminal (Git Bash or CMD)
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name person-extraction \
	--pool chula-pool \
	--params '{"table_name":"Person","output_filename":"Person.json","limit":1000}'
=====================================================================================

### ⏰ With Cron Schedule

Every hour:

put this command into the terminal (Git Bash or CMD)
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name person-extraction \
	--pool chula-pool \
	--cron "0 * * * *" \
	--params '{"table_name":"Person","output_filename":"Person.json","limit":1000}'
=====================================================================================

Daily at midnight:

put this command into the terminal (Git Bash or CMD)
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name person-extraction \
	--pool chula-pool \
	--cron "0 0 * * *" \
	--params '{"table_name":"Person","output_filename":"Person.json","limit":1000}'
=====================================================================================

### 🔁 With Interval Schedule

Every 3600 seconds (1 hour):

put this command into the terminal (Git Bash or CMD)
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name person-extraction \
	--pool chula-pool \
	--interval 3600 \
	--params '{"table_name":"Person","output_filename":"Person.json","limit":1000}'
=====================================================================================

## 📚 Common Tables Deployment Examples

put this command into the terminal (Git Bash or CMD)
==============================================
export PREFECT_API_URL=http://localhost:4200/api
==============================================

👤 Person table:
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name person-extraction \
	--pool chula-pool \
	--params '{"table_name":"Person","output_filename":"Person.json","limit":1000}'
=====================================================================================

🏢 Dept table:
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name dept-extraction \
	--pool chula-pool \
	--params '{"table_name":"Dept","output_filename":"Dept.json","limit":1000}'
=====================================================================================

🧪 EQ table:
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name eq-extraction \
	--pool chula-pool \
	--params '{"table_name":"EQ","output_filename":"EQ.json","limit":1000}'
=====================================================================================

🛠 Craft table:
=====================================================================================
python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
	--name craft-extraction \
	--pool chula-pool \
	--params '{"table_name":"Craft","output_filename":"Craft.json","limit":1000}'
=====================================================================================

## ▶️ Running a Deployment

After deployment, run it from the UI or CLI:

put this command into the terminal (Git Bash or CMD)
==============================================
export PREFECT_API_URL=http://localhost:4200/api
==============================================

put this command into the terminal (Git Bash or CMD)
============================================================
python -m prefect deployment run 'extract_chula_data/person-extraction'
============================================================

🌐 Or visit Prefect UI in browser:
============================================================
http://localhost:4200/deployments
============================================================

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

put this command into the terminal (Git Bash or CMD)
==============================================
export PREFECT_API_URL=http://localhost:4200/api
==============================================

put this command into the terminal (Git Bash or CMD)
============================================================
python -m prefect work-pool ls
============================================================

### 📋 View deployment details

put this command into the terminal (Git Bash or CMD)
==============================================
export PREFECT_API_URL=http://localhost:4200/api
==============================================

put this command into the terminal (Git Bash or CMD)
============================================================
python -m prefect deployment ls
============================================================

### 🗑 Delete a deployment

put this command into the terminal (Git Bash or CMD)
==============================================
export PREFECT_API_URL=http://localhost:4200/api
==============================================

put this command into the terminal (Git Bash or CMD)
=======================================================================
python -m prefect deployment delete 'extract_chula_data/person-extraction'
=======================================================================
