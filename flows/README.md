# Flow Organization Structure

## Current Structure

```
flows/
├── chula_extraction/              # Chula SQL Server extraction
│   ├── __init__.py
│   ├── flow_chula_extract_data.py
│   └── tasks_chula_extract_data.py
│
├── cedar7_cost_by_eq/             # Cedar7 cost_by_eq ETL (SQL Server -> PostgreSQL)
│   ├── __init__.py
│   ├── flow_cedar7_cost_by_eq.py
│   └── tasks_cedar7_cost_by_eq.py
```

## Future ETL Example

When you add a new ETL pipeline (e.g., data transformation):

```
flows/
├── chula_extraction/              # Extraction flows
│   ├── __init__.py
│   ├── flow_chula_extract_data.py
│   └── tasks_chula_extract_data.py
│
├── chula_transform/               # Transformation flows
│   ├── __init__.py
│   ├── flow_chula_clean_data.py
│   ├── tasks_chula_clean_data.py
│   └── tasks_chula_validate.py
│
├── chula_analytics/               # Analytics/aggregation
│   ├── __init__.py
│   ├── flow_chula_daily_report.py
│   └── tasks_chula_metrics.py
│
└── chula_integration/             # External integrations
    ├── __init__.py
    ├── flow_chula_api_sync.py
    └── tasks_chula_api.py
```

## Benefits

- ✅ **Isolated code** - Each flow has its own folder
- ✅ **Reusable tasks** - Tasks can be imported across flows
- ✅ **Easy navigation** - Find code by project/purpose
- ✅ **Team collaboration** - Multiple developers work on different folders
- ✅ **Testing** - Unit test each module independently

## Deployment Structure

Each flow folder has corresponding deployment:

```
deployments/
├── deploy_chula_extraction.py
├── deploy_chula_transform.py
└── deploy_chula_analytics.py
```

## Naming Convention

- **Folder**: `{project}_{purpose}/`
- **Flow file**: `flow_{project}_{action}.py`
- **Tasks file**: `tasks_{project}_{action}.py`
- **Deployment**: `deploy_{project}_{purpose}.py`

Example:
- Project: `chula`
- Purpose: `extraction`
- Action: `extract_data`
- Flow: `chula_extraction/flow_chula_extract_data.py`
