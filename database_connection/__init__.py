import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus


def _normalize_postgres_url(url: str) -> str:
    """Ensure the SQLAlchemy URL uses a sync driver for pandas operations."""
    if url is None or url.strip() == "":
        raise ValueError("PostgreSQL connection string environment variable is not set")

    if "+asyncpg" in url:
        return url.replace("+asyncpg", "+psycopg", 1)
    return url

def get_sqlserver_connection_string() -> str:
    """Get SQL Server connection string using pyodbc driver"""
    host = os.getenv('SQLSERVER_HOST')
    port = os.getenv('SQLSERVER_PORT', '1433')
    user = os.getenv('SQLSERVER_USER')
    password = os.getenv('SQLSERVER_PASSWORD')
    database = os.getenv('SQLSERVER_DATABASE')

    if ',' in host:
        host, port = host.split(',')
    params = quote_plus(
        f"DRIVER={{SQL Server}};"
        f"SERVER={host},{port};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password}"
    )

    return f"mssql+pyodbc:///?odbc_connect={params}"

def get_sqlserver_engine():
    connection_string = get_sqlserver_connection_string()
    return create_engine(connection_string)

def get_postgres_engine(env_var: str = "LOAD_DATABASE_CONNECTION_URL"):
    """Create a SQLAlchemy engine for PostgreSQL destinations."""
    raw_url = os.getenv(env_var)
    connection_url = _normalize_postgres_url(raw_url)
    return create_engine(connection_url, pool_pre_ping=True)


__all__ = [
    "get_sqlserver_engine",
    "get_sqlserver_connection_string",
    "get_postgres_engine",
]
