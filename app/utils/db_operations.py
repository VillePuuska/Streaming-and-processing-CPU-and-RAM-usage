import duckdb
import numpy as np


def get_latest_data(pg_conn: str) -> dict[str, np.array]:
    duckdb.sql(
        f"""
        INSTALL postgres;
        LOAD postgres;
        ATTACH '{pg_conn}' AS pg (TYPE POSTGRES);
        """
    )
    res = duckdb.sql("FROM pg.public.latest_measurements").fetchnumpy()
    duckdb.sql("DETACH pg")
    return res


def get_last_minute_data(pg_conn: str) -> dict[str, np.array]:
    duckdb.sql(
        f"""
        INSTALL postgres;
        LOAD postgres;
        ATTACH '{pg_conn}' AS pg (TYPE POSTGRES);
        """
    )
    res = duckdb.sql("FROM pg.public.measurements_last_minute").fetchnumpy()
    duckdb.sql("DETACH pg")
    return res
