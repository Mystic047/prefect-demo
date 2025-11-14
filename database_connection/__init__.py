import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

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

__all__ = ["get_sqlserver_engine", "get_sqlserver_connection_string"]
