from __future__ import annotations

from typing import Dict

from prefect import flow, get_run_logger

from .tasks import (
    extract_cost_by_eq_data,
    transform_cost_by_eq_data,
    load_cost_by_eq_data,
)


@flow(name="cedar7-cost-by-eq", log_prints=True)
def sync_cost_by_eq() -> Dict[str, int]:
    """Run the cedar7 cost_by_eq ETL with embedded SQL and defaults."""
    logger = get_run_logger()
    logger.info("🚀 Starting cedar7 cost_by_eq ETL")

    extracted_df = extract_cost_by_eq_data()
    transformed_df = transform_cost_by_eq_data(extracted_df)
    load_stats = load_cost_by_eq_data(
        transformed_df,
        truncate_before_load=True,
    )

    run_summary = {
        "rows_extracted": len(extracted_df),
        "rows_loaded": load_stats["rows_inserted"],
        "destination": load_stats["qualified_table"],
        "truncate_before_load": True,
    }
    logger.info("✅ ETL finished: %s", run_summary)
    return run_summary
