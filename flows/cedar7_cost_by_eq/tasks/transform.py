from __future__ import annotations

import pandas as pd
from prefect import get_run_logger, task


@task(name="cedar7-transform-cost-by-eq")
def transform_cost_by_eq_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply cedar_dashboard-specific cleanup."""
    logger = get_run_logger()
    if df.empty:
        logger.warning("No rows returned from source; skipping transformations")
        return df

    result = df.copy()
    result.columns = [col.strip().lower() for col in result.columns]

    rename_map = {
        "eqno": "eq_no",
        "eqname": "eq_name",
        "eqcode": "eq_code",
        "siteno": "site_no",
        "wotypegroupno": "wo_type_group_no",
        "mhcost": "mh_cost",
        "sparepartcost": "sparepart_cost",
        "outsourcecost": "outsource_cost",
        "maincost": "main_cost",
        "wodate": "wodate",
    }
    result = result.rename(columns=rename_map)

    result["date"] = pd.to_datetime(result["wodate"], errors="coerce")
    result["year"] = result["date"].dt.year
    result["month"] = result["date"].dt.month
    result["date"] = result["date"].dt.strftime("%Y-%m-%d")

    numeric_columns = [
        "year",
        "month",
        "site_no",
        "wo_count",
        "eq_no",
        "mh_cost",
        "sparepart_cost",
        "outsource_cost",
        "main_cost",
        "wo_type_group_no",
    ]
    for column in numeric_columns:
        if column in result.columns:
            result[column] = (
                pd.to_numeric(result[column], errors="coerce")
                .round(0)
                .fillna(0)
                .astype("Int64")
            )

    for column in ["date", "eq_code", "eq_name"]:
        if column in result.columns:
            result[column] = result[column].fillna("")

    final_columns = [
        "date",
        "year",
        "month",
        "site_no",
        "wo_count",
        "eq_no",
        "eq_code",
        "eq_name",
        "mh_cost",
        "sparepart_cost",
        "outsource_cost",
        "main_cost",
        "wo_type_group_no",
    ]
    result = result[final_columns]

    logger.info("Transformed %s rows", len(result))
    return result
