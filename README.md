# Prefect Production Setup

Clean production-ready setup for Prefect data orchestration with SQL Server and external PostgreSQL.

## Architecture

```
┌─────────────────────────────────────────────┐
│           Docker Containers                 │
│                                             │
│  ┌──────────────┐    ┌──────────────┐      │
│  │   Prefect    │    │   Prefect    │      │
│  │   Server     │◄───┤   Worker     │      │
│  │  (Port 4200) │    │ (chula-pool) │      │
│  └───────┬──────┘    └──────┬───────┘      │
│          │                  │              │
└──────────┼──────────────────┼───────────────┘
           │                  │
           ▼                  ▼
    ┌─────────────┐    ┌─────────────┐
    │ PostgreSQL  │    │ SQL Server  │
    │   (AWS)     │    │   (Azure)   │
    │             │    │             │
    │ Prefect     │    │ Your Data   │
    │  Metadata   │    │   Source    │
    └─────────────┘    └─────────────┘
```

## Folder Structure

```
prefect-demo/
├── flows/                  # Flow definitions
│   └── chula_extraction/   # Chula extraction flow package
├── database_connection/    # SQL Server connection helpers
├── scripts/                # Utility scripts
│   └── init_prefect.sh     # Database setup script (optional)
├── output/                 # Flow outputs (JSON files)
├── docker-compose.yml      # Container orchestration
├── Dockerfile              # Worker container image
├── requirements.txt        # Python dependencies
├── .env.template           # Environment variables template
├── how_to_deploy.md        # Step-by-step deploy/run commands
└── README.md               # This file
```

## Prerequisites

### 1. PostgreSQL Database (AWS RDS)

Create a PostgreSQL database for Prefect metadata:

```sql
CREATE DATABASE prefect_db;
CREATE USER prefect_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE prefect_db TO prefect_user;
```

### 2. SQL Server Database

Ensure your SQL Server is accessible and you have:
- Host/endpoint
- Port (default: 1433)
- Database name
- Username and password

## Setup Instructions

### Step 1: Configure Environment

```bash
# Copy template
cp .env.template .env

# Edit with your credentials
nano .env
```

Update these values:
```env
# PostgreSQL (Prefect metadata storage)
PREFECT_API_DATABASE_CONNECTION_URL=postgresql+asyncpg://prefect_user:your_password@your-rds-host.amazonaws.com:5432/prefect_db

# SQL Server (Your data source)
SQLSERVER_HOST=your-server.database.windows.net
SQLSERVER_PORT=1433
SQLSERVER_DATABASE=your_database
SQLSERVER_USER=your_username
SQLSERVER_PASSWORD=your_password
```

### Step 2: Start Services

```bash
docker-compose up -d
```

Verify containers are running:
```bash
docker-compose ps
```

### Step 3: Deploy and Run Flows

You now deploy flows directly from your Windows host using the Prefect CLI (no `deployments` folder). See `how_to_deploy.md` for detailed, copy-paste commands.

Basic pattern from Windows (Git Bash or CMD):

```bash
export PREFECT_API_URL=http://localhost:4200/api

python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
  --name person-extraction \
  --pool chula-pool \
  --params '{"table_name":"Person","output_filename":"Person.json","limit":1000}'

python -m prefect deployment run 'extract_chula_data/person-extraction'
```

## Flow Parameters

The main extraction flow `extract_chula_data` accepts:

- `table_name` (required): SQL Server table to extract
- `output_filename` (optional): Output JSON filename
- `limit` (optional): Max rows to extract (default: 1000)

## Output Files

Extracted data is saved to `./output/` as JSON files:
```
output/
├── Person.json
├── Dept.json
└── EQ.json
```

## Monitoring

Access Prefect UI: http://localhost:4200

- View flow runs
- Monitor logs
- Check work pool status
- Manage deployments

## Common Commands

```bash
# View logs
docker-compose logs -f prefect-worker

# Stop services
docker-compose down

# Restart worker
docker-compose restart prefect-worker

# Check work pools
docker exec prefect-server prefect work-pool ls
```

## Deployments Overview

You create and run deployments from your Windows host using the Prefect CLI.

Basic pattern:

```bash
export PREFECT_API_URL=http://localhost:4200/api

python -m prefect deploy flows/chula_extraction/flow_chula_extract_data.py:extract_chula_data \
  --name person-extraction \
  --pool chula-pool \
  --params '{"table_name":"Person","output_filename":"Person.json","limit":1000}'

python -m prefect deployment run 'extract_chula_data/person-extraction'
```

For more deployment examples (Dept, EQ, Craft, scheduling, deleting deployments), see `how_to_deploy.md`.

## Database Migration Details

Prefect automatically creates these tables in PostgreSQL:

- `flow_run` - Flow execution history
- `task_run` - Task execution details
- `deployment` - Deployment configurations
- `work_pool` - Work pool definitions
- `log` - Flow and task logs
- And many more...

No manual table creation needed!

## Troubleshooting

### Cannot connect to PostgreSQL

```bash
# Test connection
docker run --rm postgres:15-alpine psql "postgresql://user:pass@host:5432/db" -c "SELECT 1"
```

### SQL Server connection fails

Verify:
- Firewall rules allow connections
- ODBC Driver 17 is installed (included in Dockerfile)
- Connection string format is correct

### Work pool not found

```bash
# Create manually
docker exec prefect-server prefect work-pool create chula-pool --type process
```

## Production Checklist

- [ ] PostgreSQL database created on AWS RDS
- [ ] SQL Server accessible from Docker network
- [ ] `.env` file configured with real credentials
- [ ] Database migrations completed
- [ ] Work pool `chula-pool` created
- [ ] Flow deployed successfully
- [ ] Test run completed
- [ ] Monitoring in Prefect UI working

## Security Notes

- Never commit `.env` file
- Use strong passwords for database connections
- Restrict PostgreSQL access to known IPs
- Use SSL/TLS for database connections in production
- Consider using secrets management (AWS Secrets Manager, Azure Key Vault)
