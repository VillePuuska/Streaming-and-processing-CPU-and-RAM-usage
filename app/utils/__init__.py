import duckdb

duckdb.sql(
    f"""
    INSTALL postgres;
    LOAD postgres;
    """
)
