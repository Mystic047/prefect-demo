from prefect import flow, get_run_logger
from .tasks_chula_extract_data import extract_table_data, save_to_csv


@flow(name="extract_chula_data", log_prints=True)
def extract_chula_data(
    table_name: str,
    output_filename: str = None,
    limit: int = 1000
):
    logger = get_run_logger()
    logger.info(f"🚀 Starting Chula SQL Server extraction: {table_name}")
    df = extract_table_data(table_name, limit)
    if output_filename is None:
        output_filename = f"{table_name}.json"
    output_path = f"/app/output/{output_filename}"
    saved_path = save_to_csv(df, output_path)
    logger.info(f"✅ Extraction complete! File: {saved_path}")

    return {
        "table": table_name,
        "rows": len(df),
        "columns": len(df.columns),
        "output": saved_path
    }
